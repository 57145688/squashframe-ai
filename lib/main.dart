import 'dart:io';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'package:video_player/video_player.dart';
import 'package:http/http.dart' as http;
void main()=>runApp(const SquashApp());
class SquashApp extends StatelessWidget {
 const SquashApp({super.key});
 @override Widget build(BuildContext context)=>MaterialApp(title:'SquashFrame AI',theme:ThemeData.dark(useMaterial3:true),home:const AnalyzeScreen());
}
class AnalyzeScreen extends StatefulWidget {
 const AnalyzeScreen({super.key});
 @override State<AnalyzeScreen> createState()=>_AnalyzeScreenState();
}
class _AnalyzeScreenState extends State<AnalyzeScreen> {
 VideoPlayerController? video;
 String? path;
 String status='选择壁球训练视频';
 final server=TextEditingController(text:'http://192.168.1.100:8000');
 bool busy=false;
 double speed=1;
 @override void dispose(){video?.dispose();server.dispose();super.dispose();}
 Future<void> pick() async {
  final selected=await FilePicker.platform.pickFiles(type:FileType.video);
  final p=selected?.files.single.path;
  if(p==null)return;
  final next=VideoPlayerController.file(File(p));
  await next.initialize();
  await video?.dispose();
  if(!mounted)return;
  setState((){video=next;path=p;status='视频已载入';});
  next.addListener((){if(mounted)setState((){});});
 }
 Future<void> seekFrame(int direction) async {
  final v=video;
  if(v==null||!v.value.isInitialized)return;
  await v.pause();
  final ms=v.value.position.inMilliseconds+direction*33;
  await v.seekTo(Duration(milliseconds:ms.clamp(0,v.value.duration.inMilliseconds)));
 }
 Future<void> analyze() async {
  if(path==null||busy)return;
  setState((){busy=true;status='正在分析视频';});
  try {
   final request=http.MultipartRequest('POST',Uri.parse('${server.text.trim()}/analyze'))
    ..files.add(await http.MultipartFile.fromPath('video',path!));
   final response=await http.Response.fromStream(await request.send());
   if(response.statusCode!=200)throw Exception('HTTP ${response.statusCode}: ${response.body}');
   final data=jsonDecode(response.body) as Map<String,dynamic>;
   setState(()=>status='完成：检测 ${data['detected_frames']} / ${data['sampled_frames']} 帧；CSV: ${server.text}${data['csv_url']}');
  }catch(e){setState(()=>status='分析失败：$e');}
  finally{if(mounted)setState(()=>busy=false);}
 }
 @override Widget build(BuildContext context){
  final v=video;
  return Scaffold(appBar:AppBar(title:const Text('SquashFrame AI · V0.1')),body:ListView(padding:const EdgeInsets.all(16),children:[
   const Text('壁球动作分析',style:TextStyle(fontSize:24,fontWeight:FontWeight.bold)),
   const SizedBox(height:12),
   if(v!=null&&v.value.isInitialized)AspectRatio(aspectRatio:v.value.aspectRatio,child:VideoPlayer(v))
   else const SizedBox(height:220,child:Center(child:Icon(Icons.sports_tennis,size:72))),
   FilledButton.icon(onPressed:pick,icon:const Icon(Icons.video_library),label:const Text('导入视频')),
   if(v!=null&&v.value.isInitialized)...[
    Slider(value:v.value.position.inMilliseconds.toDouble().clamp(0,v.value.duration.inMilliseconds.toDouble()),max:v.value.duration.inMilliseconds.toDouble().clamp(1,double.infinity),onChanged:(n)=>v.seekTo(Duration(milliseconds:n.toInt()))),
    Row(mainAxisAlignment:MainAxisAlignment.spaceEvenly,children:[
     IconButton(onPressed:()=>seekFrame(-1),icon:const Icon(Icons.skip_previous)),
     IconButton(onPressed:()=>v.value.isPlaying?v.pause():v.play(),icon:Icon(v.value.isPlaying?Icons.pause:Icons.play_arrow)),
     IconButton(onPressed:()=>seekFrame(1),icon:const Icon(Icons.skip_next)),
     DropdownButton<double>(value:speed,items:[0.25,0.5,1.0,2.0].map((s)=>DropdownMenuItem(value:s,child:Text('${s}x'))).toList(),onChanged:(s)async{if(s==null)return;await v.setPlaybackSpeed(s);setState(()=>speed=s);})
    ])
   ],
   TextField(controller:server,decoration:const InputDecoration(labelText:'分析服务器地址')),
   FilledButton(onPressed:busy?null:analyze,child:Text(busy?'分析中':'运行姿态分析')),
   SelectableText(status)
  ]));
 }
}

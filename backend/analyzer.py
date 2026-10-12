import csv,json
from pathlib import Path
import cv2
from pose_math import angle

def analyze(video_path,output_dir,stride=3):
    import mediapipe as mp
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=True)
    cap=cv2.VideoCapture(str(video_path))
    if not cap.isOpened():raise ValueError("Cannot open video")
    fps=cap.get(cv2.CAP_PROP_FPS) or 30
    total=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    pose_mod=mp.solutions.pose
    rows=[];idx=0
    with pose_mod.Pose(model_complexity=1,min_detection_confidence=.5,min_tracking_confidence=.5) as pose:
        while True:
            ok,frame=cap.read()
            if not ok:break
            if idx%stride==0:
                res=pose.process(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
                row={'frame':idx,'time_s':round(idx/fps,3),'detected':False}
                if res.pose_landmarks:
                    lm=res.pose_landmarks.landmark
                    p=lambda n:(lm[n].x,lm[n].y)
                    P=pose_mod.PoseLandmark
                    for side in ('LEFT','RIGHT'):
                        q=lambda part:getattr(P,side+'_'+part).value
                        row[side.lower()+'_elbow_deg']=angle(p(q('SHOULDER')),p(q('ELBOW')),p(q('WRIST')))
                        row[side.lower()+'_knee_deg']=angle(p(q('HIP')),p(q('KNEE')),p(q('ANKLE')))
                    row['detected']=True
                    row['keypoints']=[{'x':v.x,'y':v.y,'visibility':v.visibility} for v in lm]
                    mp.solutions.drawing_utils.draw_landmarks(frame,res.pose_landmarks,pose_mod.POSE_CONNECTIONS)
                cv2.imwrite(str(out/f'frame_{idx:06d}.jpg'),frame)
                rows.append(row)
            idx+=1
    cap.release()
    keys=['frame','time_s','detected','left_elbow_deg','right_elbow_deg','left_knee_deg','right_knee_deg']
    with (out/'angles.csv').open('w',newline='',encoding='utf8') as f:
        writer=csv.DictWriter(f,fieldnames=keys,extrasaction='ignore');writer.writeheader();writer.writerows(rows)
    summary={'fps':fps,'frames_total':total,'sampled_frames':len(rows),'detected_frames':sum(bool(r['detected']) for r in rows),'stride':stride,'measurements':rows}
    (out/'results.json').write_text(json.dumps(summary,ensure_ascii=False),encoding='utf8')
    return {k:v for k,v in summary.items() if k!='measurements'}

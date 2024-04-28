from deepface import DeepFace

def analyze_emotion(image_path):
    try:
        analysis = DeepFace.analyze(img_path=image_path, actions=['emotion'])
        print(analysis)
        return [x["dominant_emotion"] for x in analysis]
    except Exception as e:
        return str(e)

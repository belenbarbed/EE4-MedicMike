import pickle


face_name = 'face_name.pkl'
face_enc = 'face_enc.pkl'
meh = []
with open(face_name, "wb") as fp:
    pickle.dump(meh,fp)
with open(face_enc, "wb") as fp:
    pickle.dump(meh,fp)
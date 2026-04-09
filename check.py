import joblib

# Model එක load කරමු
model = joblib.load('agri_intel_model.pkl')

# Model එකේ feature names ටික print කරලා බලමු
try:
    print("Model එකේ තියෙන ඇත්තම නම් ටික මෙන්න:")
    print(model.feature_names_in_)
except AttributeError:
    print("මෙම මොඩල් එකේ feature_names_in_Attribute එක නැත.")
    
"""
Trusted Medical Reference Library Documents.
Contains verified educational medical information from recognized global health organizations.
"""

from typing import List, Dict, Any

MEDICAL_DOCUMENTS: List[Dict[str, Any]] = [
    {
        "id": "doc_diabetes_01",
        "title": "Diabetes Mellitus: Classification, Symptoms, Causes, and Prevention",
        "source": "World Health Organization - Diabetes",
        "category": "Endocrine & Metabolic Health",
        "keywords": [
            "diabetes", "type 2 diabetes", "type 1 diabetes", "blood sugar", "glucose",
            "insulin", "hyperglycemia", "polyuria", "polydipsia", "hba1c", "lifestyle"
        ],
        "content": (
            "Diabetes mellitus is a chronic metabolic disease characterized by elevated levels of blood glucose "
            "(or blood sugar), which leads over time to serious damage to the heart, blood vessels, eyes, kidneys, and nerves. "
            "Type 1 diabetes is characterized by deficient insulin production in the pancreas and requires daily administration of insulin. "
            "Type 2 diabetes results from the body's ineffective use of insulin and accounts for more than 95% of people with diabetes.\n\n"
            "Key Symptoms:\n"
            "- Excessive thirst (polydipsia) and frequent urination (polyuria), particularly at night\n"
            "- Persistent hunger, unintended weight loss, and chronic fatigue\n"
            "- Blurred vision and slow-healing sores or frequent infections\n"
            "- Tingling, numbness, or pain in the hands or feet (peripheral neuropathy)\n\n"
            "Causes and Risk Factors:\n"
            "- Overweight, obesity, and physical inactivity\n"
            "- Genetic predisposition and family history\n"
            "- Unhealthy diet high in refined sugars and ultra-processed carbohydrates\n"
            "- Advanced age and high blood pressure\n\n"
            "Prevention and Management:\n"
            "- Maintain healthy body weight through balanced caloric intake\n"
            "- Engage in at least 150 minutes of moderate-intensity aerobic physical activity weekly\n"
            "- Adopt a diet rich in whole grains, fiber, vegetables, and lean proteins while restricting saturated fats and simple sugars\n"
            "- Avoid all tobacco use, as smoking increases the risk of cardiovascular complications\n"
            "- Regular screening with Fasting Plasma Glucose or HbA1c tests for early detection"
        )
    },
    {
        "id": "doc_hypertension_02",
        "title": "Hypertension (High Blood Pressure): Risks, Symptoms, and Lifestyle Interventions",
        "source": "American Heart Association - Understanding Blood Pressure Readings",
        "category": "Cardiovascular Health",
        "keywords": [
            "hypertension", "high blood pressure", "systolic", "diastolic", "dash diet",
            "sodium", "cardiovascular", "heart attack", "stroke", "arterial pressure"
        ],
        "content": (
            "Hypertension (high blood pressure) occurs when the force of blood flowing through your blood vessels is consistently too high. "
            "A normal blood pressure reading is less than 120/80 mm Hg. Stage 1 hypertension is diagnosed when systolic blood pressure is "
            "130-139 mm Hg or diastolic is 80-89 mm Hg.\n\n"
            "Symptoms:\n"
            "- Hypertension is often called the 'silent killer' because most individuals have no warning signs or symptoms\n"
            "- In severe hypertensive crisis (>180/120 mm Hg), symptoms can include severe headaches, chest pain, dizziness, "
            "shortness of breath, nausea, vomiting, vision changes, or nosebleeds\n\n"
            "Causes and Modifiable Risk Factors:\n"
            "- High dietary sodium intake (>2,000 mg/day) and low potassium consumption\n"
            "- Sedentary lifestyle and obesity\n"
            "- Excessive alcohol consumption and tobacco use\n"
            "- Chronic psychological stress and sleep apnea\n\n"
            "Prevention and Non-Pharmacological Management:\n"
            "- Follow the Dietary Approaches to Stop Hypertension (DASH) eating plan (rich in fruits, vegetables, whole grains, low-fat dairy)\n"
            "- Limit sodium intake to under 1,500 - 2,300 mg per day\n"
            "- Participate in 30 minutes of aerobic exercise 5 days per week\n"
            "- Limit alcohol consumption and eliminate tobacco smoking\n"
            "- Monitor blood pressure at home using validated upper-arm monitors"
        )
    },
    {
        "id": "doc_asthma_03",
        "title": "Asthma: Triggers, Management Guidelines, and Emergency Indicators",
        "source": "Global Initiative for Asthma (GINA) - Patient Guidelines",
        "category": "Respiratory Health",
        "keywords": [
            "asthma", "wheezing", "inhaler", "bronchospasm", "airway", "shortness of breath",
            "allergies", "corticosteroid", "bronchodilator", "peak flow"
        ],
        "content": (
            "Asthma is a major noncommunicable chronic disease characterized by recurrent attacks of breathlessness and wheezing, "
            "which vary in severity and frequency from person to person. During an asthma attack, the lining of the bronchial tubes swells, "
            "causing the airways to narrow and reducing the flow of air into and out of the lungs.\n\n"
            "Symptoms:\n"
            "- Recurrent wheezing, whistling sound when breathing out\n"
            "- Coughing, especially at night or early morning, or during exercise\n"
            "- Shortness of breath and tightness or pressure in the chest\n\n"
            "Common Triggers:\n"
            "- Indoor allergens (house dust mites, pet dander, mold)\n"
            "- Outdoor allergens (pollens and grasses)\n"
            "- Environmental irritants (tobacco smoke, chemical fumes, air pollution, cold air)\n"
            "- Viral respiratory infections and strenuous physical exertion\n\n"
            "Management and Action Plan:\n"
            "- Use daily maintenance anti-inflammatory inhalers (inhaled corticosteroids) as prescribed to prevent attacks\n"
            "- Keep fast-acting rescue bronchodilator inhalers (such as albuterol) accessible at all times\n"
            "- Develop a personalized written Asthma Action Plan with a healthcare provider\n"
            "- Identify and systematically avoid individual environmental triggers\n\n"
            "Emergency Warning Signs Requiring Urgent Medical Care:\n"
            "- Severe shortness of breath or inability to speak in complete sentences\n"
            "- Bluish lips or fingernails (cyanosis) indicating inadequate oxygenation\n"
            "- Chest retractions (skin sucking in around ribs or collarbone during inhalation)\n"
            "- Failure of fast-acting rescue inhaler to relieve symptoms within 10 to 15 minutes"
        )
    },
    {
        "id": "doc_cold_flu_04",
        "title": "Common Cold vs. Influenza (Flu): Clinical Distinctions and Recovery Guidance",
        "source": "Centers for Disease Control and Prevention (CDC) - Cold Versus Flu",
        "category": "Infectious & Respiratory Diseases",
        "keywords": [
            "cold", "flu", "influenza", "viral infection", "fever", "cough", "sore throat",
            "runny nose", "body aches", "vaccine", "antiviral"
        ],
        "content": (
            "The common cold and influenza are both contagious viral respiratory illnesses, but they are caused by different viruses. "
            "Because cold and flu share many symptoms, it can be difficult (or even impossible) to tell the difference based on symptoms alone, "
            "though flu symptoms are generally far more intense and have a rapid onset.\n\n"
            "Distinguishing Characteristics:\n"
            "- Onset: Influenza has an abrupt, sudden onset (within hours), whereas colds develop gradually over 1 to 3 days\n"
            "- Fever: Common and high (100°F - 104°F) with flu, lasting 3-4 days; rare and mild with a cold\n"
            "- Body Aches and Fatigue: Severe body aches, chills, and profound fatigue are hallmark signs of influenza; colds involve mild aches\n"
            "- Respiratory Symptoms: Runny or stuffy nose and sneezing are prominent in colds; flu focuses more on dry cough, chest discomfort, and headache\n\n"
            "Prevention and Care:\n"
            "- Annual influenza vaccination is the single most effective way to prevent flu and reduce severity\n"
            "- Frequent hand washing with soap and water for at least 20 seconds, or alcohol-based hand rub\n"
            "- Hydration with water, broths, and electrolyte solutions; plenty of restorative bed rest\n"
            "- Over-the-counter fever reducers and analgesics (e.g., acetaminophen, ibuprofen) for symptom relief\n"
            "- Note: Antibiotics do not work against viral infections like the cold or flu\n\n"
            "When to Seek Immediate Medical Evaluation:\n"
            "- Difficulty breathing or persistent shortness of breath\n"
            "- Persistent chest or abdominal pain\n"
            "- High fever unresponsive to antipyretics or lasting more than 4 days\n"
            "- Extreme weakness, dizziness, confusion, or inability to stay hydrated"
        )
    },
    {
        "id": "doc_cardiovascular_05",
        "title": "Cardiovascular Disease Prevention: Heart Health and Warning Signs",
        "source": "American Heart Association - Lifestyle Guidelines for Cardiovascular Risk Reduction",
        "category": "Cardiovascular Health",
        "keywords": [
            "heart disease", "cardiovascular", "cholesterol", "ldl", "atherosclerosis",
            "heart attack", "myocardial infarction", "stroke", "coronary artery"
        ],
        "content": (
            "Cardiovascular diseases (CVDs) remain the leading cause of death globally. Most cardiovascular diseases can be prevented "
            "by addressing behavioral risk factors such as tobacco use, unhealthy diet and obesity, physical inactivity, and harmful alcohol use.\n\n"
            "Key Preventive Recommendations (Life's Essential 8):\n"
            "- Eat a heart-healthy diet rich in whole foods, vegetables, fruits, lean poultry, nuts, and healthy plant oils (olive oil)\n"
            "- Engage in 150 minutes of moderate aerobic exercise or 75 minutes of vigorous exercise each week\n"
            "- Avoid smoking and vaping; eliminate exposure to second-hand tobacco smoke\n"
            "- Maintain healthy sleep duration (7 to 9 hours nightly for adults)\n"
            "- Control weight, blood lipids (cholesterol), blood glucose, and blood pressure\n\n"
            "Recognizing Heart Attack Symptoms (Seek Emergency Care Immediately - Call 911/112):\n"
            "- Chest discomfort or pressure: uncomfortable pressure, squeezing, fullness, or pain in the center of the chest lasting more than a few minutes\n"
            "- Discomfort radiating to other areas of the upper body, such as one or both arms, the back, neck, jaw, or stomach\n"
            "- Shortness of breath, with or without chest discomfort\n"
            "- Cold sweat, unexplained nausea, lightheadedness, or sudden extreme fatigue (frequently reported in women)"
        )
    },
    {
        "id": "doc_covid19_06",
        "title": "COVID-19 (SARS-CoV-2): Symptoms, Transmission, and Preventive Measures",
        "source": "World Health Organization - Coronavirus Disease (COVID-19) Guidance",
        "category": "Infectious & Respiratory Diseases",
        "keywords": [
            "covid-19", "coronavirus", "sars-cov-2", "respiratory", "vaccination",
            "mask", "isolation", "loss of taste", "loss of smell", "transmission"
        ],
        "content": (
            "Coronavirus disease 2019 (COVID-19) is an infectious illness caused by the SARS-CoV-2 virus. Most people infected with the virus "
            "will experience mild to moderate respiratory illness and recover without requiring special treatment, but some become seriously ill.\n\n"
            "Common Symptoms:\n"
            "- Fever, dry cough, and fatigue\n"
            "- Loss of taste (ageusia) or loss of smell (anosmia)\n"
            "- Sore throat, headache, body aches, diarrhea, and nasal congestion\n\n"
            "Preventive Protocols:\n"
            "- Keep up to date with COVID-19 vaccinations and booster doses\n"
            "- Ensure adequate ventilation and airflow in indoor spaces\n"
            "- Practice proper respiratory etiquette (coughing/sneezing into bent elbow)\n"
            "- Maintain hand hygiene with alcohol-based sanitizers or handwashing\n"
            "- Wear a well-fitting, high-filtration mask (e.g., N95, KN95) in crowded indoor public settings\n"
            "- Stay home and self-isolate if feeling unwell or testing positive to protect others\n\n"
            "Emergency Signs Requiring Urgent Medical Care:\n"
            "- Difficulty breathing or persistent pain/pressure in the chest\n"
            "- New confusion or inability to wake or stay awake\n"
            "- Pale, gray, or blue skin, lips, or nail beds depending on skin tone"
        )
    },
    {
        "id": "doc_lifestyle_07",
        "title": "Comprehensive Preventive Wellness: Nutrition, Hydration, Sleep, and Physical Health",
        "source": "Trusted Medical Reference Library",
        "category": "General Preventive Health",
        "keywords": [
            "preventive health", "wellness", "nutrition", "hydration", "water intake",
            "sleep hygiene", "exercise", "mental wellness", "routine screening"
        ],
        "content": (
            "Preventive healthcare involves proactive measures taken for disease prevention rather than disease treatment. "
            "Evidence-based lifestyle medicine emphasizes foundational pillars of health to prevent chronic noncommunicable illnesses.\n\n"
            "Foundational Wellness Pillars:\n"
            "1. Nutrition: Emphasize a diverse plant-forward diet rich in dietary fiber (25-35g daily), antioxidants, lean proteins, "
            "and omega-3 fatty acids, while minimizing processed meats, trans-fats, and added sugars.\n"
            "2. Hydration: Drink adequate fluids (typically 2 to 3 liters daily for average adults, adjusting for climate and exertion) "
            "to support metabolic functions, kidney health, and cognitive performance.\n"
            "3. Sleep Hygiene: Prioritize 7 to 9 hours of uninterrupted sleep per night. Maintain a consistent sleep schedule and minimize "
            "blue light screen exposure before bedtime.\n"
            "4. Physical Activity: Combine aerobic exercise (walking, swimming, cycling) with resistance/strength training 2 days per week "
            "to maintain muscle mass, metabolic sensitivity, and bone density.\n"
            "5. Routine Screenings: Schedule regular health checks for blood pressure, lipid profile, fasting blood glucose, and age-appropriate "
            "cancer screenings (e.g., mammograms, colonoscopies).\n\n"
            "Safety Reminder: Lifestyle modifications support overall health but do not replace prescribed therapies or medical advice."
        )
    }
]

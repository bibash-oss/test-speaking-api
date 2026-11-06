"""
Official OET Nursing speaking role-play scenarios (50 complete cases).
All scenarios have Candidate role = Nurse and strictly adhere to the exact pattern:
{
  "setting": "...",
  "timings": {"speaking_time": 300, "preparation_time": 180},
  "patient_card": {"tasks": [...], "description": "..."},
  "candidate_card": {"role": "Nurse", "tasks": [...], "description": "..."}
}
"""

OET_NURSING_SCENARIOS = [   {   'content': {   'candidate_card': {   'description': 'You are a ward nurse attending to a 68-year-old patient '
                                                            'on Day 1 following an elective total knee arthroplasty '
                                                            '(TKA). The physiotherapist is scheduled to assist with '
                                                            'mobilization, but the patient is in significant pain and '
                                                            'adamantly refusing to get out of bed.',
                                             'role': 'Nurse',
                                             'tasks': [   "Introduce yourself and inquire about the patient's current "
                                                          'comfort and pain level using a 0–10 scale.',
                                                          "Acknowledge the patient's distress and validate their fear "
                                                          'of worsening the surgical knee.',
                                                          'Explain the clinical importance of early mobilization '
                                                          '(preventing DVT, chest infection, joint stiffness).',
                                                          'Offer appropriate breakthrough analgesia 30 minutes before '
                                                          'physiotherapy.',
                                                          'Reassure the patient about physical support, walking aids, '
                                                          'and gradual pacing.',
                                                          'Check understanding and confirm the agreed plan for pain '
                                                          'relief and mobilization.']},
                       'patient_card': {   'description': 'You are a 68-year-old patient on Day 1 after an elective '
                                                          'total knee replacement. You are experiencing severe '
                                                          'surgical pain (8/10) when moving and are terrified that '
                                                          'bending or stepping on your leg will tear the surgical '
                                                          'stitches or damage the new implant. You are reluctant to '
                                                          'take strong painkillers for fear of addiction.',
                                           'tasks': [   'Explain to the nurse that the pain in your knee is unbearable '
                                                        '(8/10) and you cannot face walking.',
                                                        'Describe your fear that moving or bending the leg will rip '
                                                        'your stitches or dislocate the implant.',
                                                        'Ask whether you can stay in bed until tomorrow when it might '
                                                        'hurt less.',
                                                        'Express your concern that stronger painkillers will make you '
                                                        'confused or addicted.',
                                                        'Ask whether a walking frame will give enough support so you '
                                                        "don't fall.",
                                                        'Reluctantly agree to try walking once the nurse offers '
                                                        'pre-medication analgesia and explains clot prevention.']},
                       'setting': 'Orthopedic Surgical Ward',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'MEDIUM',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Post-Operative Knee Arthroplasty Mobilization and Pain Relief'},
    {   'content': {   'candidate_card': {   'description': 'You are a discharge nurse speaking to a 42-year-old '
                                                            'patient who underwent an uncomplicated laparoscopic '
                                                            'cholecystectomy earlier this morning. The patient is '
                                                            'anxious about sharp right shoulder pain.',
                                             'role': 'Nurse',
                                             'tasks': [   'Welcome the patient and assess their current symptoms and '
                                                          'questions.',
                                                          'Explain the physiological cause of referred shoulder-tip '
                                                          'pain (diaphragmatic irritation from carbon dioxide gas '
                                                          'insufflation).',
                                                          'Provide practical home relief strategies (gentle walking, '
                                                          'heat packs, resting semi-recumbent, prescribed analgesia).',
                                                          'Explain post-operative incision care and signs of wound '
                                                          'infection (redness, purulent discharge, fever).',
                                                          'Advise when to resume normal activities and when to seek '
                                                          'urgent medical attention.',
                                                          'Provide a discharge booklet and confirm patient '
                                                          'understanding.']},
                       'patient_card': {   'description': 'You are a 42-year-old patient 4 hours after a laparoscopic '
                                                          'gallbladder removal. Your stomach cuts are sore (3/10), but '
                                                          'your right shoulder has a sharp, stabbing pain (6/10) that '
                                                          'worsens when lying flat. You worry something was damaged '
                                                          'during surgery.',
                                           'tasks': [   'Explain your symptoms to the nurse, especially the sharp pain '
                                                        'in your right shoulder.',
                                                        'Describe how the shoulder pain worsens when you lie flat on '
                                                        'the bed.',
                                                        'Express concern that the surgeon accidentally damaged a nerve '
                                                        'or organ in your chest.',
                                                        'Ask why your shoulder hurts if the surgery was performed on '
                                                        'your abdomen.',
                                                        'Ask how long this shoulder pain will last and how to relieve '
                                                        'it at home.',
                                                        'Ask when you can take a shower and remove the waterproof '
                                                        'dressings.']},
                       'setting': 'Day Surgery Unit',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'EASY',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Post-Laparoscopic Cholecystectomy Discharge and Shoulder-Tip Pain'},
    {   'content': {   'candidate_card': {   'description': 'You are a breast care nurse speaking to a 47-year-old '
                                                            'woman on Day 2 following a unilateral modified radical '
                                                            'mastectomy with axillary node clearance. She is tearful, '
                                                            'struggling to look at her surgical wound, and overwhelmed '
                                                            'by her Jackson-Pratt drain.',
                                             'role': 'Nurse',
                                             'tasks': [   'Introduce yourself warmly and demonstrate sensitive, '
                                                          "non-hurried empathy toward the patient's distress.",
                                                          'Acknowledge the physical and emotional impact of mastectomy '
                                                          'and validate her feelings of loss and grief.',
                                                          'Explain the purpose and safe home management of the suction '
                                                          'drain (milking, measuring output, keeping bulb compressed).',
                                                          'Discuss wound healing, soft cotton front-fastening bras, '
                                                          'and temporary prostheses.',
                                                          'Introduce community support services (breast care nurse '
                                                          'follow-up, cancer support groups, psychological '
                                                          'counseling).',
                                                          'Establish next steps for drain removal criteria (output < '
                                                          '30 mL over 24 hours).']},
                       'patient_card': {   'description': 'You are a 47-year-old woman on Day 2 after a left modified '
                                                          'radical mastectomy. You feel devastated by the loss of your '
                                                          'breast, terrified to look at the incision, and anxious '
                                                          'about managing the blood drainage bottle at home.',
                                           'tasks': [   'Express your deep grief and distress to the nurse about '
                                                        'losing your breast.',
                                                        'Describe your anxiety about looking in the mirror or having '
                                                        'your partner see your scar.',
                                                        'Express fear that managing the plastic suction bulb and '
                                                        'drainage tube at home will be too difficult.',
                                                        'Ask whether the drain tube could accidentally pull out while '
                                                        'you are sleeping.',
                                                        'Ask when you can be fitted for a bra and prosthesis so your '
                                                        'clothes fit normally.',
                                                        'Ask how soon you will receive the pathology results regarding '
                                                        'your lymph nodes.']},
                       'setting': 'Surgical Oncology Inpatient Ward',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'HARD',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Post-Mastectomy Drain Care and Emotional Body Image Reassurance'},
    {   'content': {   'candidate_card': {   'description': 'You are caring for a 59-year-old patient who underwent an '
                                                            'open partial lobectomy yesterday. The patient has a heavy '
                                                            'smoking history and is refusing to perform incentive '
                                                            'spirometry or coughing exercises because of surgical '
                                                            'incision pain.',
                                             'role': 'Nurse',
                                             'tasks': [   'Introduce yourself and ask the patient how their breathing '
                                                          'and incision pain feel today.',
                                                          'Acknowledge the pain caused by deep breathing and coughing '
                                                          'after chest surgery.',
                                                          'Explain the high risk of post-operative atelectasis and '
                                                          'pneumonia, particularly with a history of smoking.',
                                                          "Demonstrate the 'splinting' technique (holding a pillow "
                                                          'firmly against the wound during deep breathing and '
                                                          'coughing).',
                                                          'Optimize analgesia schedule (taking oral or PCA pain relief '
                                                          'before respiratory exercises).',
                                                          'Set achievable goals (10 breaths per hour with the '
                                                          'spirometer) and check understanding.']},
                       'patient_card': {   'description': 'You are a 59-year-old patient on Day 1 after lung surgery '
                                                          '(lobectomy). You have smoked for 35 years. Every deep '
                                                          'breath feels like your chest is tearing open (7/10 pain). '
                                                          'You believe breathing shallowly and resting quietly is the '
                                                          'safest way to heal.',
                                           'tasks': [   'Explain to the nurse that inhaling deeply feels like your '
                                                        'chest stitches are ripping apart.',
                                                        'Describe your belief that resting quietly and breathing '
                                                        'shallowly is safer for your healing.',
                                                        'Ask whether coughing forcefully will pop your chest staples '
                                                        'or burst an internal stitch.',
                                                        'Ask whether you can just be given oxygen through a mask '
                                                        'instead of using the plastic breathing tube.',
                                                        'Agree to try the breathing tube using the pillow-splinting '
                                                        'technique after receiving pain medication.']},
                       'setting': 'Cardiothoracic Post-Surgical Ward',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'MEDIUM',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Refusal of Incentive Spirometry and Deep Breathing Exercises'},
    {   'content': {   'candidate_card': {   'description': 'You are preparing a 24-year-old university student for '
                                                            'discharge following an emergency laparoscopic '
                                                            'appendectomy performed 24 hours ago. The patient lives '
                                                            'alone in shared student accommodation.',
                                             'role': 'Nurse',
                                             'tasks': [   "Introduce yourself and confirm the patient's readiness for "
                                                          'discharge.',
                                                          'Explain wound care: keeping surgical dressing dry for 48 '
                                                          'hours, patting dry after showering, avoiding '
                                                          'bathing/swimming.',
                                                          'Highlight red-flag infection symptoms (spreading redness, '
                                                          'warmth, fever >38°C, increasing pain, foul-smelling '
                                                          'discharge).',
                                                          'Discuss activity restrictions (avoiding heavy lifting >5kg, '
                                                          'contact sports, and driving for 2 weeks).',
                                                          'Advise on bowel regularity and prevention of constipation '
                                                          'from opioid analgesia.',
                                                          'Provide contact details for the ward and emergency '
                                                          'department, and check understanding.']},
                       'patient_card': {   'description': 'You are a 24-year-old university student being discharged 1 '
                                                          'day after emergency appendix removal. You feel mostly fine '
                                                          'but live with busy flatmates who are out all day, so you '
                                                          'are nervous about managing on your own.',
                                           'tasks': [   'Explain to the nurse that you live in shared student housing '
                                                        'and will be alone during the day.',
                                                        'Describe your current pain (mild, 2/10) and ask what '
                                                        'painkillers you can take at home.',
                                                        'Ask whether you can go to the gym and play basketball with '
                                                        'friends next week.',
                                                        'Ask how you will know if the internal incisions become '
                                                        'infected.',
                                                        "Ask what you should do if you haven't had a bowel movement "
                                                        'for several days after surgery.',
                                                        'Confirm you understand the warning signs that require '
                                                        'returning to the hospital.']},
                       'setting': 'General Surgical Ward',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'EASY',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Post-Appendectomy Discharge Care and Infection Red Flags'},
    {   'content': {   'candidate_card': {   'description': 'You are a registered nurse administering evening '
                                                            'medications to a 56-year-old patient on Day 2 '
                                                            'post-hemicolectomy. The patient refuses their daily '
                                                            'prophylactic enoxaparin (Clexane) injection due to '
                                                            'abdominal bruising and needle soreness.',
                                             'role': 'Nurse',
                                             'tasks': [   'Approach the patient respectfully and acknowledge their '
                                                          'objection to the injection.',
                                                          'Inspect the injection sites and validate their concern '
                                                          'regarding abdominal bruising.',
                                                          'Explain the critical clinical purpose of prophylactic '
                                                          'anticoagulation (preventing deep vein thrombosis and '
                                                          'life-threatening pulmonary embolism).',
                                                          'Discuss safe injection techniques (rotating sites to upper '
                                                          'arms or thighs, not rubbing the area after injection).',
                                                          'Offer comfort measures (ice pack application prior to '
                                                          'injection, slow administration).',
                                                          'Re-evaluate patient consent and document the agreed '
                                                          'approach collaboratively.']},
                       'patient_card': {   'description': 'You are a 56-year-old patient on Day 2 after bowel surgery. '
                                                          'Your stomach has painful purple bruises from the last two '
                                                          'injections. You are walking around your room and feel that '
                                                          'you no longer need blood-thinner shots in your belly.',
                                           'tasks': [   'Refuse the injection and show the nurse the purple bruises on '
                                                        'your abdomen.',
                                                        'Describe your needle phobia and how tender your stomach '
                                                        'feels.',
                                                        'Ask whether the bruises mean you are bleeding internally from '
                                                        'the surgery.',
                                                        'Ask why you still need blood thinners if you are already '
                                                        'walking to the bathroom.',
                                                        'Ask whether you can take a blood-thinner pill instead of '
                                                        'having a shot.',
                                                        'Agree to have the injection in your outer thigh with an ice '
                                                        'pack after the nurse explains the risk of blood clots.']},
                       'setting': 'Acute Colorectal Surgical Ward',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'MEDIUM',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Refusal of Subcutaneous Low-Molecular-Weight Heparin (Enoxaparin)'},
    {   'content': {   'candidate_card': {   'description': 'You are an admissions nurse checking in a 53-year-old '
                                                            'patient scheduled for an elective laparoscopic inguinal '
                                                            'hernia repair in 90 minutes. During fasting checks, the '
                                                            'patient casually mentions drinking a large mug of tea '
                                                            'with whole milk and eating a biscuit 2 hours ago.',
                                             'role': 'Nurse',
                                             'tasks': [   'Clarify the exact timing, quantity, and nature of what the '
                                                          'patient ingested.',
                                                          'Explain the physiological risk of pulmonary aspiration '
                                                          'during general anesthesia in clear terms.',
                                                          "Show empathy for the patient's frustration, as they took "
                                                          'time off work and arranged transportation.',
                                                          'Explain the hospital policy regarding clear fluids vs. milk '
                                                          'and solids (minimum 6 hours for solids/milk).',
                                                          'Discuss immediate next steps: informing the anesthetist, '
                                                          'exploring potential delay to the afternoon list rather than '
                                                          'outright cancellation.',
                                                          'Answer questions, maintain professional composure, and '
                                                          'provide reassurance.']},
                       'patient_card': {   'description': 'You are a 53-year-old self-employed builder. You are booked '
                                                          'for hernia repair at 9:00 AM. At 7:00 AM, you had a cup of '
                                                          'tea with milk and half a biscuit to wash down your blood '
                                                          'pressure pill, thinking fasting only meant skipping heavy '
                                                          'breakfast.',
                                           'tasks': [   'Mention casually to the nurse that you had a cup of milky tea '
                                                        'and a small biscuit at 7:00 AM.',
                                                        'Express disbelief when told this breaches fasting rules, '
                                                        'arguing it was only a splash of milk.',
                                                        'Express your worry that your surgery will be cancelled, '
                                                        "causing you to lose a week's income.",
                                                        'Ask why milk and biscuits are dangerous under general '
                                                        'anesthesia.',
                                                        'Ask whether the doctor can just delay the operation to this '
                                                        'afternoon instead of cancelling.',
                                                        'Agree to wait patiently in the day lounge while the nurse '
                                                        'consults the anesthetist.']},
                       'setting': 'Day Surgery Pre-Operative Admissions',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'HARD',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Pre-Operative Fasting Breach Prior to Elective Hernia Repair'},
    {   'content': {   'candidate_card': {   'description': 'You are a diabetes educator nurse consulting with a '
                                                            '51-year-old long-distance truck driver with poorly '
                                                            'controlled Type 2 Diabetes (HbA1c 10.2%). The physician '
                                                            'has prescribed once-daily basal insulin, but the patient '
                                                            'is terrified of needles and believes insulin means their '
                                                            'life is over.',
                                             'role': 'Nurse',
                                             'tasks': [   "Introduce yourself and explore the patient's feelings and "
                                                          'beliefs regarding starting insulin.',
                                                          'Acknowledge their anxiety and dismantle common myths '
                                                          "(insulin is not a personal failure, doesn't cause blindness "
                                                          'or kidney failure).',
                                                          'Demonstrate the modern insulin pen device, highlighting the '
                                                          'ultra-fine 4mm needle (thinner than a hair).',
                                                          'Offer a painless demonstration injection using sterile '
                                                          "saline on an injection pad or nurse's arm.",
                                                          'Explain hypoglycemia signs (shakiness, sweating, hunger) '
                                                          "and practical management ('Rule of 15').",
                                                          'Address workplace and driving concerns (DVLA/licensing '
                                                          'requirements and blood glucose logbook).']},
                       'patient_card': {   'description': 'You are a 51-year-old truck driver with diabetes. Maximum '
                                                          'pills are no longer working. You watched your uncle suffer '
                                                          'complications after going on insulin, and you have had a '
                                                          'severe needle phobia since childhood. You are terrified you '
                                                          'will lose your truck driving license.',
                                           'tasks': [   'Tell the nurse you cannot take insulin because you have an '
                                                        'intense fear of needles.',
                                                        'Describe how your uncle went on insulin and ended up with an '
                                                        'amputated foot.',
                                                        'Express concern that starting insulin means your diabetes is '
                                                        'in its end stages.',
                                                        'Ask whether taking insulin will cause you to fail your heavy '
                                                        'vehicle commercial driving medical.',
                                                        'Ask how you will know if your blood sugar drops dangerously '
                                                        'low while driving on the highway.',
                                                        'Agree to try a test injection with the tiny 4mm pen needle '
                                                        'once the nurse demonstrates it.']},
                       'setting': 'Community Health Diabetes Clinic',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'HARD',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Type 2 Diabetes: New Insulin Initiation and Needle Phobia'},
    {   'content': {   'candidate_card': {   'description': 'You are a respiratory specialist nurse conducting a '
                                                            'discharge consultation for a 65-year-old retired factory '
                                                            'worker being discharged after an acute exacerbation of '
                                                            'Chronic Obstructive Pulmonary Disease (COPD). The patient '
                                                            'has been using their inhaler incorrectly for years.',
                                             'role': 'Nurse',
                                             'tasks': [   "Introduce yourself and assess the patient's current "
                                                          'breathing and recovery progress.',
                                                          'Review their current inhaler technique and identify errors '
                                                          '(firing into the mouth without a spacer, inhaling too '
                                                          'fast).',
                                                          'Explain the mechanical benefits of using a spacer device '
                                                          '(delivers medicine deep into the lower airways instead of '
                                                          'the back of the throat).',
                                                          'Provide step-by-step instructions for MDI + spacer (shake, '
                                                          'insert, single actuation, slow deep breath in over 4-5 '
                                                          'seconds, hold breath for 10 seconds or tidal breathing).',
                                                          'Emphasize rinsing mouth with water after steroid inhalers '
                                                          'to prevent oral thrush and hoarseness.',
                                                          "Check patient understanding through a 'teach-back' "
                                                          'demonstration.']},
                       'patient_card': {   'description': 'You are a 65-year-old retired factory worker with severe '
                                                          'COPD, recovering from a chest flare-up. You have always '
                                                          'sprayed your inhaler directly into your mouth and feel the '
                                                          'bulky plastic spacer tube looks ridiculous and unnecessary.',
                                           'tasks': [   'Tell the nurse that the large plastic spacer tube looks '
                                                        "clumsy and you've managed without it for years.",
                                                        'Describe how you currently spray the inhaler into your mouth '
                                                        'while inhaling through your nose.',
                                                        'Mention that you frequently get white, sore spots on your '
                                                        'tongue and throat.',
                                                        'Ask why the medicine needs a spacer if spraying directly into '
                                                        'the mouth tastes so strong.',
                                                        'Ask what you should do at home if your chest suddenly '
                                                        'tightens up during the night.',
                                                        'Demonstrate using the spacer device back to the nurse after '
                                                        'the instructions.']},
                       'setting': 'Respiratory Medical Ward',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'MEDIUM',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'COPD Discharge Education and Correct Inhaler Spacer Technique'},
    {   'content': {   'candidate_card': {   'description': 'You are a practice nurse conducting an annual '
                                                            'cardiovascular review for a 57-year-old accountant. '
                                                            "Today's blood pressure is 164/98 mmHg. The patient admits "
                                                            'they stop taking their prescribed Ramipril whenever they '
                                                            "'feel energetic and normal'.",
                                             'role': 'Nurse',
                                             'tasks': [   'Welcome the patient and share the current blood pressure '
                                                          'reading empathetically.',
                                                          "Explore the patient's reasons for stopping their "
                                                          'antihypertensive medication intermittently.',
                                                          "Explain that hypertension is a 'silent condition' that "
                                                          'causes vascular damage without overt symptoms.',
                                                          'Clarify long-term risks of uncontrolled blood pressure '
                                                          '(stroke, myocardial infarction, renal impairment).',
                                                          'Discuss dietary modifications (reducing processed food, '
                                                          'limiting daily sodium to <2g, incorporating the DASH diet).',
                                                          'Collaborate on adherence strategies (pill organizer, '
                                                          'morning routine pairing, home BP diary).']},
                       'patient_card': {   'description': 'You are a 57-year-old accountant with high blood pressure '
                                                          '(164/98 mmHg). You only take your blood pressure tablets '
                                                          'when you feel stressed or have a headache, because you '
                                                          "don't like taking chemicals when you feel healthy.",
                                           'tasks': [   'Explain to the nurse that you feel completely healthy and '
                                                        'only take pills when you feel tense.',
                                                        'Describe your daily diet, which includes salty snacks, '
                                                        'takeaways, and soy sauce.',
                                                        'Express concern that taking blood pressure medication every '
                                                        'single day will make your body dependent on it.',
                                                        'Ask how high blood pressure can damage your body if you have '
                                                        'zero symptoms.',
                                                        'Ask whether reducing salt in your cooking can replace taking '
                                                        'pills altogether.',
                                                        'Agree to take the Ramipril tablet every morning with '
                                                        'breakfast and keep a home blood pressure log.']},
                       'setting': 'General Practice / Primary Care Clinic',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'MEDIUM',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Hypertension Medication Non-Adherence and Dietary Sodium Reduction'},
    {   'content': {   'candidate_card': {   'description': 'You are a specialist cardiac nurse reviewing a '
                                                            '72-year-old patient with congestive heart failure (NYHA '
                                                            'Class III) who was discharged from hospital last week. '
                                                            'The patient complains bitterly that the 1.5-litre daily '
                                                            "fluid restriction is 'torture' and admits they skipped "
                                                            'daily weigh-ins.',
                                             'role': 'Nurse',
                                             'tasks': [   'Greet the patient warmly and validate the difficulty of '
                                                          'living with strict fluid limits.',
                                                          'Explain the physiological mechanism of fluid overload in '
                                                          'heart failure (weakened heart muscle leads to fluid '
                                                          'retention in lungs and ankles).',
                                                          'Offer practical thirst-management tips (ice chips, lemon '
                                                          'wedges, mouth spray, chewing sugar-free gum, tracking '
                                                          'fluids with a jug).',
                                                          'Emphasize the vital importance of morning daily weights '
                                                          '(same scale, after voiding, before breakfast) as an early '
                                                          'warning system.',
                                                          'Define the action threshold (weight gain >1.5 kg in 24 '
                                                          'hours or >2 kg in a week = call the clinic for diuretic '
                                                          'adjustment).',
                                                          'Check understanding and provide encouraging '
                                                          'reinforcement.']},
                       'patient_card': {   'description': 'You are a 72-year-old retired gardener with congestive '
                                                          'heart failure. You find the 1.5-litre daily fluid '
                                                          'restriction nearly unbearable, especially in warm weather, '
                                                          'and you stopped weighing yourself every morning because you '
                                                          'find it pointless.',
                                           'tasks': [   'Explain to the nurse that your mouth feels completely parched '
                                                        'and 1.5 litres of water is not enough.',
                                                        'Describe how difficult it is to socialize with friends when '
                                                        "you can't have a cup of tea.",
                                                        "Admit that you haven't been checking your weight on the "
                                                        'bathroom scale every morning.',
                                                        'Ask why drinking an extra glass of water causes your ankles '
                                                        'to swell or lungs to congest.',
                                                        'Ask what practical tricks can help relieve intense mouth '
                                                        'dryness without drinking excess water.',
                                                        'Agree to start logging your morning weight in the heart '
                                                        'booklet and report any gain over 1.5 kg.']},
                       'setting': 'Heart Failure Outpatient Clinic',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'HARD',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Congestive Heart Failure: Fluid Restriction and Daily Weigh-Ins'},
    {   'content': {   'candidate_card': {   'description': 'You are a nephrology nurse consulting with a 61-year-old '
                                                            'patient recently diagnosed with Stage 3b Chronic Kidney '
                                                            'Disease (eGFR 38 mL/min). Recent blood tests show serum '
                                                            'potassium at 5.3 mmol/L. The patient is confused because '
                                                            'they thought fruits like bananas and oranges were '
                                                            'healthy.',
                                             'role': 'Nurse',
                                             'tasks': [   'Introduce yourself and review the recent blood test results '
                                                          'clearly and reassuringly.',
                                                          'Explain the role of the kidneys in filtering potassium and '
                                                          'the cardiac risks of elevated potassium (hyperkalemia).',
                                                          'Clarify which foods are high in potassium (bananas, '
                                                          'oranges, potatoes, tomatoes, dried fruit) and provide '
                                                          'lower-potassium alternatives (apples, berries, cabbage, '
                                                          'cucumbers).',
                                                          'Explain cooking techniques to reduce potassium (leaching '
                                                          'potatoes in water, boiling instead of roasting).',
                                                          'Warn against using salt substitutes (which contain '
                                                          'potassium chloride).',
                                                          'Provide a renal diet leaflet, arrange a dietitian '
                                                          'appointment, and check understanding.']},
                       'patient_card': {   'description': 'You are a 61-year-old patient with Stage 3b kidney disease. '
                                                          'Your recent blood test shows high potassium (5.3 mmol/L). '
                                                          'You love eating bananas, oranges, and baked potatoes '
                                                          'because you believed fresh fruit and vegetables were the '
                                                          'healthiest choices.',
                                           'tasks': [   'Express your confusion to the nurse about how fresh fruits '
                                                        'like bananas can be harmful.',
                                                        'Describe your daily diet, which includes daily bananas, '
                                                        'tomato sauces, and potato dishes.',
                                                        'Mention that you recently switched to Lo-Salt potassium salt '
                                                        'substitute thinking it was heart-healthy.',
                                                        'Ask whether high potassium means your kidneys have completely '
                                                        'failed and you need dialysis.',
                                                        'Ask which fruits and vegetables are safe lower-potassium '
                                                        'alternatives.',
                                                        'Agree to stop using potassium-based salt substitutes and '
                                                        'attend a renal dietitian consultation.']},
                       'setting': 'Renal Outpatient Clinic',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'MEDIUM',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Chronic Kidney Disease: Potassium and Sodium Dietary Restrictions'},
    {   'content': {   'candidate_card': {   'description': 'You are an adolescent community nurse speaking to a '
                                                            '16-year-old competitive soccer player who had an asthma '
                                                            'flare-up during training yesterday. The teenager hides '
                                                            'their blue reliever inhaler in their gym bag and avoids '
                                                            'taking their daily preventer because they are embarrassed '
                                                            'in front of teammates.',
                                             'role': 'Nurse',
                                             'tasks': [   'Establish a welcoming, non-judgmental rapport with the '
                                                          'adolescent.',
                                                          'Explore their feelings about having asthma and their sports '
                                                          'performance goals.',
                                                          'Differentiate between preventer (corticosteroid) and '
                                                          'reliever (Salbutamol) inhalers in simple sports-relevant '
                                                          'terms.',
                                                          'Address peer stigma by highlighting famous athletes and '
                                                          'soccer stars with asthma (e.g., David Beckham).',
                                                          'Co-create a discreet asthma management plan (taking '
                                                          'preventer at home morning/night, pre-exercise reliever '
                                                          'dose).',
                                                          'Check understanding and provide an updated digital/card '
                                                          'asthma action plan.']},
                       'patient_card': {   'description': 'You are a 16-year-old high school soccer player. You '
                                                          'recently had an asthma flare-up during training. You hide '
                                                          'your blue inhaler in your gym locker and stopped taking '
                                                          'your daily preventer because you are embarrassed in front '
                                                          'of teammates.',
                                           'tasks': [   "Explain to the nurse that you don't want your soccer "
                                                        'teammates seeing you use an inhaler.',
                                                        'Describe how your chest tightens up during the second half of '
                                                        'matches.',
                                                        'Mention that you stopped taking your morning preventer puff '
                                                        'because you thought you were cured.',
                                                        'Ask whether taking a steroid preventer will stunt your growth '
                                                        'or bulk you up unnaturally.',
                                                        'Ask how you can take your medication discreetly without being '
                                                        'teased in the dugout.',
                                                        'Agree to take your preventer at home morning and night, and '
                                                        'take two puffs of reliever before kickoff.']},
                       'setting': 'School / Adolescent Health Community Clinic',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'HARD',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Adolescent Asthma: Overcoming Denial and Peer Stigma'},
    {   'content': {   'candidate_card': {   'description': 'You are a rheumatology clinical nurse teaching a '
                                                            '38-year-old graphic designer how to self-administer '
                                                            'weekly subcutaneous Methotrexate via an auto-injector '
                                                            'pen. The patient had severe nausea on oral tablets and is '
                                                            'nervous about self-injecting.',
                                             'role': 'Nurse',
                                             'tasks': [   "Introduce yourself and explore the patient's past "
                                                          'experience with oral methotrexate.',
                                                          'Explain the benefits of subcutaneous injection over oral '
                                                          'tablets (superior absorption, significantly reduced '
                                                          'gastrointestinal nausea).',
                                                          'Demonstrate the auto-injector step-by-step (checking '
                                                          'window, cleaning site with alcohol swab, 90-degree angle, '
                                                          'waiting for the second click, holding for 5 seconds).',
                                                          'Discuss proper sharps disposal (yellow sharps container, '
                                                          'never in regular household trash).',
                                                          'Review essential precautions (weekly dosing only—never '
                                                          'daily, Folic acid supplementation schedule, routine '
                                                          'liver/FBC blood monitoring).',
                                                          'Have the patient walk through the steps and check '
                                                          'understanding.']},
                       'patient_card': {   'description': 'You are a 38-year-old graphic designer with rheumatoid '
                                                          'arthritis. Your rheumatologist switched you from oral '
                                                          'methotrexate tablets (which caused severe nausea) to weekly '
                                                          'subcutaneous injections. You are frightened of '
                                                          'self-injecting.',
                                           'tasks': [   'Explain to the nurse that oral methotrexate made you '
                                                        'violently nauseous for two days every week.',
                                                        'Describe your fear of giving yourself an injection with an '
                                                        'auto-injector pen.',
                                                        'Ask whether the injection pen will cause the same terrible '
                                                        'nausea as the tablets.',
                                                        'Ask what happens if you accidentally press the button too '
                                                        'soon or flinch during the injection.',
                                                        'Ask why methotrexate is taken only once a week and what '
                                                        'happens if taken on consecutive days.',
                                                        'Practice an injection using a training pen and agree to '
                                                        'self-administer your weekly dose on Sundays.']},
                       'setting': 'Rheumatology Outpatient Clinic',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'MEDIUM',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Rheumatoid Arthritis: Subcutaneous Methotrexate Auto-Injector Training'},
    {   'content': {   'candidate_card': {   'description': 'You are a practice nurse conducting an anticoagulation '
                                                            'education session for a 64-year-old patient newly '
                                                            'prescribed Warfarin for non-valvular atrial fibrillation. '
                                                            'The patient is confused about why their blood needs '
                                                            "frequent testing and heard they can't eat any green "
                                                            'vegetables.',
                                             'role': 'Nurse',
                                             'tasks': [   'Welcome the patient and assess their baseline understanding '
                                                          'of Warfarin.',
                                                          'Explain the purpose of Warfarin (thins blood to prevent '
                                                          'stroke from clot formation in atrial fibrillation).',
                                                          'Explain what INR (International Normalized Ratio) is and '
                                                          'why regular monitoring is necessary (target range 2.0–3.0).',
                                                          'Clarify the Vitamin K dietary myth: explain that green '
                                                          "leafy vegetables don't need to be eliminated, but intake "
                                                          'must remain consistent.',
                                                          'Highlight bleeding precautions and red flags (unusual '
                                                          'bruising, black tarry stools, prolonged nosebleeds, blood '
                                                          'in urine).',
                                                          'Emphasize carrying an anticoagulant alert card and '
                                                          'reporting new medications or OTC supplements.']},
                       'patient_card': {   'description': 'You are a 64-year-old patient newly diagnosed with atrial '
                                                          'fibrillation and started on Warfarin. You are alarmed '
                                                          "because a neighbor called Warfarin 'rat poison', said you "
                                                          'cannot eat any salads, and warned you will bleed to death '
                                                          'from a papercut.',
                                           'tasks': [   'Tell the nurse that you heard Warfarin is rat poison and ask '
                                                        'if it is truly safe for humans.',
                                                        'Describe your worry about having blood drawn every week for '
                                                        'INR testing.',
                                                        'Express your dismay that you might have to completely cut '
                                                        'green leafy salads from your diet.',
                                                        'Ask what exact level of bleeding requires going straight to '
                                                        'the emergency department.',
                                                        'Ask whether you can take over-the-counter painkillers like '
                                                        'ibuprofen if you get a headache.',
                                                        'Agree to keep your green vegetable intake steady and carry an '
                                                        'anticoagulant medical alert card.']},
                       'setting': 'Anticoagulation Outpatient Clinic',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'MEDIUM',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Warfarin Anticoagulation Therapy: INR Monitoring and Dietary Vitamin K'},
    {   'content': {   'candidate_card': {   'description': 'You are a pediatric triage nurse attending to a frantic '
                                                            '28-year-old mother whose 18-month-old toddler suffered a '
                                                            'simple febrile convulsion lasting 90 seconds during a '
                                                            'viral illness. The child is now post-ictal, sleeping '
                                                            'peacefully in the cot, but the mother is trembling and '
                                                            'sobbing.',
                                             'role': 'Nurse',
                                             'tasks': [   'Provide immediate, compassionate emotional containment for '
                                                          'the mother.',
                                                          "Reassure her about the child's current stable condition "
                                                          '(vitals normal, safe sleep).',
                                                          'Explain the benign nature of simple febrile convulsions '
                                                          '(triggered by rapid rise in temperature, not brain damage '
                                                          'or epilepsy).',
                                                          'Provide practical first-aid steps if a seizure occurs again '
                                                          '(stay calm, place child on side/recovery position, clear '
                                                          'area, time seizure, call emergency services if >5 minutes).',
                                                          'Clarify fever management (comfort measures, loose clothing, '
                                                          'appropriate weight-based paracetamol/ibuprofen, avoid cold '
                                                          'water sponging).',
                                                          "Confirm the doctor's pending full examination to locate the "
                                                          "viral source, and check mother's understanding."]},
                       'patient_card': {   'description': 'You are the 28-year-old mother of 18-month-old Leo. During '
                                                          'a viral fever, Leo had a 90-second convulsion where his '
                                                          'eyes rolled back and limbs jerked. Leo is now sleeping '
                                                          'peacefully in the cot, but you are sobbing and convinced he '
                                                          'has epilepsy or brain damage.',
                                           'tasks': [   'Describe the terrifying moment Leo started convulsing and why '
                                                        'you thought he was dying.',
                                                        'Express your intense fear that this convulsion has '
                                                        'permanently damaged his brain or caused epilepsy.',
                                                        'Ask whether Leo will have another seizure tonight while '
                                                        'sleeping at home.',
                                                        'Ask whether you should place him in a cold ice bath when his '
                                                        'fever spikes.',
                                                        'Ask what exact steps you must take if a convulsion ever '
                                                        'happens again.',
                                                        'Accept reassurance that simple febrile seizures do not cause '
                                                        'brain damage, and learn proper fever management.']},
                       'setting': 'Pediatric Emergency Department',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'HARD',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Pediatric Febrile Convulsion: Parental Panic and Fever Management'},
    {   'content': {   'candidate_card': {   'description': 'You are a child health nurse seeing a 31-year-old mother '
                                                            'who has brought her 12-month-old daughter for her routine '
                                                            '1-year developmental check. The mother wants to skip the '
                                                            'MMR (Measles, Mumps, Rubella) vaccine because of '
                                                            'anti-vaccine posts she read in an online parenting group.',
                                             'role': 'Nurse',
                                             'tasks': [   "Acknowledge the mother's desire to protect her child "
                                                          'without being dismissive or confrontational.',
                                                          'Explore her specific worries regarding the MMR vaccine.',
                                                          'Address the autism myth directly, explaining the history of '
                                                          'the discredited 1998 Wakefield paper and subsequent global '
                                                          'studies involving millions of children proving no link.',
                                                          'Explain the real risks of measles (pneumonia, encephalitis, '
                                                          'subacute sclerosing panencephalitis) and herd immunity.',
                                                          'Discuss common mild post-vaccine reactions (mild fever, '
                                                          'faint rash 7-10 days later) and how to manage them.',
                                                          'Encourage shared decision-making, offer an informative '
                                                          'leaflet, and invite her to proceed with vaccination.']},
                       'patient_card': {   'description': 'You are a 31-year-old mother attending your 12-month-old '
                                                          "daughter's checkup. You want to skip the MMR vaccine "
                                                          'because you read posts on a parenting forum claiming the '
                                                          'triple shot causes autism and overloads toddler immune '
                                                          'systems.',
                                           'tasks': [   'Explain to the nurse that you want to delay or skip the MMR '
                                                        'vaccine due to safety concerns.',
                                                        'Describe what you read online about healthy toddlers '
                                                        'regressing into autism after the MMR jab.',
                                                        'Ask why you cannot give the measles, mumps, and rubella '
                                                        'vaccines as separate individual shots.',
                                                        'Ask why your daughter needs the vaccine if measles is '
                                                        'relatively rare in your local area.',
                                                        'Ask what common side effects might occur 7 to 10 days after '
                                                        'the MMR vaccination.',
                                                        'Agree to proceed with the vaccination after the nurse '
                                                        'explains the debunked research and real measles risks.']},
                       'setting': 'Maternal and Child Health Clinic',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'HARD',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Childhood Immunization Hesitancy: Addressing MMR Autism Concerns'},
    {   'content': {   'candidate_card': {   'description': 'You are a dermatology nurse consulting with the mother of '
                                                            'a 3-year-old boy suffering from severe atopic dermatitis '
                                                            'with lichenified, bleeding excoriations in the flexural '
                                                            'creases. The GP prescribed 1% hydrocortisone cream, but '
                                                            'the mother refuses to apply it due to fears of skin '
                                                            'thinning.',
                                             'role': 'Nurse',
                                             'tasks': [   "Inspect the child's skin gently and acknowledge the "
                                                          "mother's daily exhaustion dealing with itchy eczema.",
                                                          "Directly address 'topical steroid phobia', explaining that "
                                                          'mild over-the-counter steroids used as directed do not '
                                                          'cause systemic damage or skin thinning.',
                                                          'Explain the Fingertip Unit (FTU) method to ensure accurate '
                                                          'and safe dosing.',
                                                          'Emphasize the foundation of eczema care: liberal, frequent '
                                                          'application of bland emollients (ointments rather than '
                                                          'lotions).',
                                                          'Advise on bathing techniques (short lukewarm baths, patting '
                                                          'dry, applying emollient within 3 minutes).',
                                                          'Check understanding and provide an eczema action plan.']},
                       'patient_card': {   'description': 'You are the mother of a 3-year-old boy suffering from '
                                                          'severe atopic eczema with bleeding scratches on his knees '
                                                          'and elbows. You refuse to apply prescribed 1% '
                                                          'hydrocortisone cream because you fear it will thin his skin '
                                                          'and stunt his growth.',
                                           'tasks': [   'Explain to the nurse how terribly your son scratches and '
                                                        'suffers every night from itchy eczema.',
                                                        'Express your fear that applying steroid cream will thin his '
                                                        'delicate skin or absorb into his organs.',
                                                        'Mention that you have been trying natural coconut oil and '
                                                        "herbal creams, but they aren't working.",
                                                        "Ask how much steroid cream is safe to use so you don't "
                                                        'accidentally overdose him.',
                                                        'Ask how often and how thickly moisturizing emollient '
                                                        'ointments should be applied.',
                                                        'Agree to use the steroid cream using the Fingertip Unit rule '
                                                        'for short flare-up bursts.']},
                       'setting': 'Pediatric Outpatient Dermatology Clinic',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'MEDIUM',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Pediatric Atopic Eczema: Topical Steroid Phobia and Emollient Care'},
    {   'content': {   'candidate_card': {   'description': 'You are a midwife / postnatal nurse visiting a '
                                                            '30-year-old primiparous mother on Day 3 following an '
                                                            'uncomplicated vaginal birth. The patient is crying in '
                                                            'bed, experiencing breast engorgement and cracked nipples, '
                                                            "and expresses feeling like a 'terrible mother'.",
                                             'role': 'Nurse',
                                             'tasks': [   'Provide a warm, supportive presence and normalize Day 3 '
                                                          "'baby blues' due to rapid postpartum hormonal shifts.",
                                                          'Acknowledge the physical pain of breast engorgement and '
                                                          'sore nipples.',
                                                          'Assess infant latch and position (ensuring wide open mouth, '
                                                          'flanged lips, taking in the lower areola).',
                                                          'Offer practical engorgement relief (warm compress before '
                                                          'feeding, reverse pressure softening, cool compresses or '
                                                          'cabbage leaves after feeds).',
                                                          'Discuss nipple care (expressing drops of breastmilk, '
                                                          'purified lanolin, air drying).',
                                                          'Provide contact details for community lactation consultants '
                                                          'and infant feeding support groups.']},
                       'patient_card': {   'description': 'You are a 30-year-old first-time mother on Day 3 after '
                                                          'normal birth. Your breasts are engorged, rock-hard, and '
                                                          'painful (7/10). Latching makes your cracked nipples bleed, '
                                                          'and you cannot stop crying, feeling like a complete failure '
                                                          'as a mother.',
                                           'tasks': [   'Break down in tears and explain to the midwife that feeding '
                                                        'hurts like razor blades.',
                                                        'Describe how rock-hard and painfully swollen your breasts '
                                                        'feel since your milk came in.',
                                                        'Express feelings of guilt and inadequacy that you are failing '
                                                        'your newborn baby.',
                                                        'Ask why you cannot stop crying when you should be happy (baby '
                                                        'blues).',
                                                        'Ask what practical relief measures will soften your breasts '
                                                        'before the baby latches.',
                                                        'Ask whether you should give up breastfeeding and switch to '
                                                        'formula bottles.']},
                       'setting': 'Postnatal Inpatient Maternity Ward',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'MEDIUM',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Postnatal Ward: Engorgement, Sore Nipples, and Baby Blues'},
    {   'content': {   'candidate_card': {   'description': 'You are a triage nurse speaking to the father of a '
                                                            '2-year-old girl who has had vomiting and watery diarrhea '
                                                            'for 24 hours. The father has been giving large bottles of '
                                                            'apple juice and flat lemonade, which has made the '
                                                            'diarrhea worse.',
                                             'role': 'Nurse',
                                             'tasks': [   "Assess the child's current hydration status (wet nappies, "
                                                          'tears, alertness, mucous membranes).',
                                                          'Explain why sugary drinks like apple juice and lemonade '
                                                          'worsen diarrhea (osmotic effect drawing water into the '
                                                          'bowel).',
                                                          'Introduce Oral Rehydration Solutions (ORS, e.g., Dioralyte) '
                                                          'and explain their balanced sodium/glucose mechanism.',
                                                          'Detail the administration technique (small, frequent '
                                                          'amounts: 5 mL by syringe or teaspoon every 5 minutes rather '
                                                          'than large gulps).',
                                                          'Highlight red flags requiring immediate emergency hospital '
                                                          'review (lethargy, sunken eyes, no wet nappy in 8 hours, '
                                                          'blood in stool, persistent vomiting).',
                                                          "Check father's understanding and provide an ORS starter "
                                                          'pack.']},
                       'patient_card': {   'description': 'You are the father of 2-year-old Chloe, who has had '
                                                          'vomiting and watery diarrhea for 24 hours. You have been '
                                                          'giving her large cups of undiluted apple juice and flat '
                                                          'lemonade to keep her energy up, but she keeps throwing up.',
                                           'tasks': [   "Explain your daughter's vomiting and diarrhea to the triage "
                                                        'nurse.',
                                                        'Describe how you have been giving her apple juice and '
                                                        'lemonade to keep her hydrated.',
                                                        'Mention that she had a wet nappy 3 hours ago and still '
                                                        'produces tears when crying.',
                                                        'Ask why apple juice is making her diarrhea worse when it is '
                                                        'natural fruit juice.',
                                                        'Ask how to give oral rehydration solution (Dioralyte) without '
                                                        'Chloe vomiting it back up.',
                                                        'Ask what warning signs mean Chloe is severely dehydrated and '
                                                        'needs hospital admission.']},
                       'setting': 'Community Health Pediatric Clinic',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'EASY',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Pediatric Acute Gastroenteritis: Oral Rehydration Therapy'},
    {   'content': {   'candidate_card': {   'description': 'You are a pediatric triage nurse attending to a '
                                                            'frightened mother whose 2-year-old son woke up at '
                                                            "midnight with a harsh, barking 'seal-like' cough and "
                                                            'hoarse voice. The child has received an oral dose of '
                                                            'Dexamethasone and is resting comfortably, but the mother '
                                                            'is fearful of nighttime breathing distress.',
                                             'role': 'Nurse',
                                             'tasks': [   "Assess the child's respiratory effort (absence of stridor "
                                                          'at rest, chest indrawing, respiratory rate).',
                                                          'Reassure the mother and explain what croup '
                                                          '(laryngotracheobronchitis) is in plain language (viral '
                                                          'swelling of the voice box).',
                                                          'Explain the role of the steroid medication (Dexamethasone) '
                                                          'in reducing airway inflammation over the next several '
                                                          'hours.',
                                                          'Discuss home comforting measures (calm environment, upright '
                                                          'posture, cool night air or bathroom steam).',
                                                          'Clearly define critical red flags (stridor at rest, sternal '
                                                          'retractions/rib indrawing, pale or blue skin, drooling, '
                                                          'difficulty swallowing).',
                                                          'Check understanding and provide clear safety-net '
                                                          'instructions.']},
                       'patient_card': {   'description': 'You are the mother of 2-year-old Noah. He woke up at 1:00 '
                                                          'AM with a harsh, barking seal-like cough and stridor. The '
                                                          'doctor gave him oral steroid syrup 30 minutes ago, but you '
                                                          'are terrified his windpipe will swell completely shut when '
                                                          'you go home.',
                                           'tasks': [   'Describe the terrifying seal-bark cough and hoarse breathing '
                                                        'that woke your toddler.',
                                                        'Express fear that his throat will swell completely shut when '
                                                        'you return home tonight.',
                                                        'Ask how long the oral steroid syrup (Dexamethasone) takes to '
                                                        'reduce the airway swelling.',
                                                        'Ask what home comforting measures (cool night air, upright '
                                                        'posture, bathroom steam) help croup.',
                                                        'Ask what exact breathing signs (stridor at rest, chest '
                                                        'retractions) require calling an ambulance.',
                                                        'Feel reassured after the nurse explains the viral croup '
                                                        'course and safety-net signs.']},
                       'setting': 'Urgent Care Centre',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'MEDIUM',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Pediatric Croup: Barking Cough, Cool Mist, and Stridor Red Flags'},
    {   'content': {   'candidate_card': {   'description': 'You are a pediatric diabetes nurse consulting with the '
                                                            'anxious mother of an 8-year-old boy recently diagnosed '
                                                            'with Type 1 Diabetes. The boy is returning to primary '
                                                            'school next week, and the mother is terrified that the '
                                                            'teachers will fail to recognize or treat low blood sugar '
                                                            '(hypoglycemia).',
                                             'role': 'Nurse',
                                             'tasks': [   "Empathize with the mother's anxiety regarding relinquishing "
                                                          'constant supervision at school.',
                                                          'Explain the collaborative School Healthcare Plan (formal '
                                                          'communication with teachers, sports coaches, and school '
                                                          'nurse).',
                                                          'Review hypoglycemia symptoms in children (pallor, '
                                                          'shakiness, sweating, irritability, glassy eyes, confusion).',
                                                          'Explain the Hypo Kit contents (fast-acting glucose: fruit '
                                                          'juice poppers, jelly beans, followed by complex '
                                                          'carbohydrates like crackers).',
                                                          'Explain emergency Glucagon nasal powder (Baqsimi) or '
                                                          'injection and when 999/emergency services must be called.',
                                                          'Empower the mother with reassurance and schedule a school '
                                                          'visit.']},
                       'patient_card': {   'description': 'You are the mother of 8-year-old Toby, newly diagnosed with '
                                                          'Type 1 Diabetes. Toby returns to primary school next week. '
                                                          "You are so terrified that teachers won't recognize low "
                                                          'blood sugar (hypo) that you are planning to sit outside his '
                                                          'classroom all day.',
                                           'tasks': [   'Explain your overwhelming anxiety about Toby returning to '
                                                        'school with Type 1 Diabetes.',
                                                        'Describe the symptoms Toby displays when his blood sugar '
                                                        'drops low (pale, shaky, irritable).',
                                                        'Express fear that his teachers will miss a severe hypo during '
                                                        'busy classroom activities.',
                                                        "Ask what emergency supplies should be kept in Toby's "
                                                        'classroom Hypo Box.',
                                                        'Ask how school staff should administer emergency nasal '
                                                        'glucagon (Baqsimi) if Toby passes out.',
                                                        'Agree to a school healthcare meeting where the nurse will '
                                                        "train Toby's teachers."]},
                       'setting': 'Community Pediatric Endocrinology Clinic',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'HARD',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Pediatric Type 1 Diabetes: Managing Hypoglycemia at School'},
    {   'content': {   'candidate_card': {   'description': 'You are a school nurse consulting with an embarrassed '
                                                            'mother whose 7-year-old daughter was found to have active '
                                                            'head lice during a classroom notification. The mother is '
                                                            "scrubbing her daughter's scalp raw with harsh antiseptics "
                                                            'and feels ashamed.',
                                             'role': 'Nurse',
                                             'tasks': [   'Provide a warm, reassuring environment and dismantle the '
                                                          'social stigma (head lice prefer clean hair; not a sign of '
                                                          'poor hygiene or bad parenting).',
                                                          'Advise against harsh household chemicals or abrasive '
                                                          "scrubbing which damages the child's scalp.",
                                                          'Explain evidence-based treatments: topical pediculicide '
                                                          '(e.g., 5% Permethrin or Dimeticone) or wet combing '
                                                          'conditioner method.',
                                                          'Explain the life cycle of lice and the crucial importance '
                                                          'of a second treatment 7 days later to kill newly hatched '
                                                          'nymphs.',
                                                          'Advise on family screening and environmental cleaning (wash '
                                                          'pillowcases/brushes in hot water; no need for fumigating '
                                                          'the house).',
                                                          'Clarify school return policy (child can return immediately '
                                                          'after the first treatment).']},
                       'patient_card': {   'description': 'You are the mother of 7-year-old Lily. You received a '
                                                          'school notification that Lily has head lice. You are '
                                                          'scrubbing her head with harsh Dettol disinfectant, feeling '
                                                          'mortified, ashamed, and worried that other parents will '
                                                          'think your home is dirty.',
                                           'tasks': [   'Express your embarrassment and shame to the school nurse '
                                                        'about Lily having head lice.',
                                                        'Describe how vigorously you have been scrubbing her hair with '
                                                        'antiseptic and washing every sheet.',
                                                        'Ask whether head lice mean your home is dirty or that you are '
                                                        'a bad mother.',
                                                        'Ask which pharmacy treatment (Dimeticone or Permethrin) is '
                                                        'safest and most effective.',
                                                        'Ask why a second treatment is strictly necessary 7 days after '
                                                        'the first application.',
                                                        'Ask whether Lily needs to be kept home from school until '
                                                        'every single egg is combed out.']},
                       'setting': 'Primary School Health Clinic',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'EASY',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Pediatric Head Lice (Pediculosis Capitis): Eradication and Social Stigma'},
    {   'content': {   'candidate_card': {   'description': 'You are a senior triage nurse speaking to the angry, '
                                                            'pacing 35-year-old brother of a patient who sprained his '
                                                            'ankle playing recreational basketball. They have been '
                                                            'waiting for 2.5 hours on a busy Saturday night, and the '
                                                            'brother is demanding immediate physician attention.',
                                             'role': 'Nurse',
                                             'tasks': [   'De-escalate the situation: maintain calm, non-defensive '
                                                          'posture, use open body language, and listen actively.',
                                                          'Acknowledge their frustration and validate the discomfort '
                                                          'of waiting.',
                                                          'Explain the Manchester Triage System objectively (patients '
                                                          'are prioritized by clinical urgency and life-threat, such '
                                                          'as cardiac arrests and severe trauma, not order of '
                                                          'arrival).',
                                                          'Offer comfort measures for the injured patient (ice pack, '
                                                          'elevation, oral analgesia, reassessing the ankle).',
                                                          'Set realistic expectations regarding estimated wait times '
                                                          'without making false promises.',
                                                          'Establish boundaries against verbal abuse while reassuring '
                                                          'that the patient has not been forgotten.']},
                       'patient_card': {   'description': 'You are the 35-year-old brother of a patient with a twisted '
                                                          'ankle. You have been waiting in the emergency department '
                                                          'waiting room for 2.5 hours on a busy Saturday night, and '
                                                          'you are pacing angrily, demanding your brother be seen '
                                                          'immediately.',
                                           'tasks': [   'Express your anger and frustration to the triage nurse about '
                                                        'waiting nearly three hours.',
                                                        'Complain that people who arrived after you are being called '
                                                        'through to the treatment rooms first.',
                                                        "Express concern that your brother's swollen ankle could "
                                                        'suffer permanent joint damage.',
                                                        'Ask why no one has provided an ice pack, painkillers, or an '
                                                        'estimated waiting time.',
                                                        'Listen as the nurse explains the clinical triage system and '
                                                        'life-threatening emergencies.',
                                                        'De-escalate your anger when provided with an ice pack, oral '
                                                        'analgesia, and a realistic timeframe.']},
                       'setting': 'Emergency Department Waiting Room',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'HARD',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Emergency Department Waiting Times and De-Escalating an Aggressive Relative'},
    {   'content': {   'candidate_card': {   'description': 'You are an allergy clinical nurse consulting with a '
                                                            '21-year-old university student who was discharged from ED '
                                                            'yesterday following an anaphylactic reaction to trace '
                                                            'peanuts in a Thai curry. The patient has been prescribed '
                                                            'two EpiPen (0.3mg Adrenaline) auto-injectors.',
                                             'role': 'Nurse',
                                             'tasks': [   'Introduce yourself and review the recent allergic event '
                                                          'empathetically.',
                                                          'Explain the difference between mild allergy (hives, lip '
                                                          'itch) and life-threatening anaphylaxis (throat tightness, '
                                                          'wheeze, dizziness).',
                                                          "Demonstrate EpiPen technique using a trainer device: 'Blue "
                                                          "to the sky, orange to the thigh', swing and push firmly at "
                                                          '90 degrees, hold for 3 seconds, massage site.',
                                                          'Emphasize the golden rule: ALWAYS call 999/emergency '
                                                          'services immediately after administering adrenaline.',
                                                          'Explain the rationale for carrying two pens at all times '
                                                          '(second dose after 5-15 minutes if symptoms persist).',
                                                          'Have the patient demonstrate back using the trainer pen, '
                                                          'and check understanding.']},
                       'patient_card': {   'description': 'You are a 21-year-old university student who suffered an '
                                                          'anaphylactic reaction to peanut oil at a restaurant '
                                                          'yesterday. You were given two EpiPen auto-injectors on '
                                                          'discharge, but you are terrified of self-injecting and '
                                                          "worried the bulky pens won't fit in your pocket.",
                                           'tasks': [   'Describe the terrifying throat tightness and difficulty '
                                                        'breathing you experienced yesterday.',
                                                        'Express your anxiety about giving yourself a needle injection '
                                                        'into your thigh muscle.',
                                                        'Ask how you will know when an allergic reaction is bad enough '
                                                        'to justify using the EpiPen.',
                                                        'Ask why you must call emergency services (999) immediately '
                                                        'after using the adrenaline pen.',
                                                        'Ask why you were prescribed two pens and whether you must '
                                                        'carry both everywhere you go.',
                                                        'Practice with a trainer EpiPen device and demonstrate the '
                                                        "'blue to sky, orange to thigh' technique."]},
                       'setting': 'Allergy and Immunology Outpatient Clinic',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'MEDIUM',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Anaphylaxis and EpiPen Auto-Injector Training for Young Adult'},
    {   'content': {   'candidate_card': {   'description': 'You are an emergency nurse preparing discharge '
                                                            'instructions for a 23-year-old amateur soccer player who '
                                                            'suffered a brief concussive head strike during a match. '
                                                            'Normal CT head, GCS 15. The patient wants to drive '
                                                            'himself home and go to a pub with friends tonight.',
                                             'role': 'Nurse',
                                             'tasks': [   "Assess the patient's current symptoms (headache, dizziness, "
                                                          'photophobia).',
                                                          'Explain that he cannot drive himself home or stay alone '
                                                          'tonight; a responsible adult must observe him for 24 hours.',
                                                          'Provide clear head injury warning signs that necessitate an '
                                                          'immediate return to the ED (worsening severe headache, '
                                                          'repeated vomiting, unequal pupils, confusion, seizure, '
                                                          'fluid leaking from nose/ears).',
                                                          'Advise on cognitive and physical rest (avoiding screens, '
                                                          'alcohol, sedatives, and contact sports for at least 2 '
                                                          'weeks).',
                                                          'Discuss gradual return-to-sport protocols.',
                                                          'Provide a head injury written checklist and confirm patient '
                                                          'understanding.']},
                       'patient_card': {   'description': 'You are a 23-year-old amateur rugby player who had a brief '
                                                          '10-second knockout during a match. Your emergency CT head '
                                                          'scan is clear. You want to drive your car home alone and '
                                                          'meet your friends at the pub for a pint tonight.',
                                           'tasks': [   'Tell the nurse you feel fine now, your scan was clear, and '
                                                        'you plan to drive yourself home.',
                                                        'Describe your minor frontal headache (3/10) and ask if you '
                                                        'can take ibuprofen.',
                                                        'Express confusion when told you cannot stay alone tonight or '
                                                        'drink alcohol with friends.',
                                                        'Ask why drinking alcohol or driving is dangerous if the brain '
                                                        'scan showed no bleeding.',
                                                        'Ask when you can return to playing full-contact rugby matches '
                                                        'with your team.',
                                                        'Agree to call your brother to pick you up and follow the '
                                                        'written head-injury warning checklist.']},
                       'setting': 'Emergency Department Observation Unit',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'MEDIUM',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Minor Head Injury / Concussion Discharge Advice and Red Flags'},
    {   'content': {   'candidate_card': {   'description': 'You are a practice nurse dressing a 10cm superficial '
                                                            'partial-thickness burn on the dorsal forearm of a '
                                                            '29-year-old chef caused by boiling oil splash 2 hours '
                                                            'ago. The patient wants to pop the blisters and return to '
                                                            'the kitchen tonight.',
                                             'role': 'Nurse',
                                             'tasks': [   'Examine the wound, check tetanus immunization status, and '
                                                          'assess pain.',
                                                          'Explain the crucial biological role of intact burn blisters '
                                                          '(natural sterile biological barrier preventing severe '
                                                          'bacterial infection).',
                                                          'Advise against unproven home remedies (butter, ice, '
                                                          'toothpaste) and explain appropriate burn first-aid (20 '
                                                          'minutes cool running tap water).',
                                                          'Explain the non-adherent dressing plan (e.g., silicone mesh '
                                                          '+ absorbent pad) and keeping it clean and dry.',
                                                          'Provide clinical rationale why working in a hot, greasy '
                                                          'commercial kitchen tonight poses an extreme infection risk.',
                                                          'Schedule a wound review in 48 hours and check '
                                                          'understanding.']},
                       'patient_card': {   'description': 'You are a 29-year-old sous chef with a second-degree burn '
                                                          'blister on your forearm from hot cooking oil. You want the '
                                                          'nurse to pop the blisters, put a bandage on, and let you '
                                                          'return to the kitchen for the busy Saturday dinner service.',
                                           'tasks': [   'Show the painful blisters on your forearm to the nurse and '
                                                        'ask to have them popped.',
                                                        'Explain that your head chef will be furious if you miss the '
                                                        'Saturday night dinner rush.',
                                                        "Ask why intact burn blisters shouldn't be popped to let the "
                                                        'wound dry out faster.',
                                                        'Ask why working in a hot, greasy commercial kitchen poses a '
                                                        'severe infection risk.',
                                                        'Ask how to care for the burn dressing in the shower and '
                                                        'whether it will leave an ugly scar.',
                                                        'Accept medical leave for 3 days and agree to keep the '
                                                        'dressing intact and dry.']},
                       'setting': 'Urgent Care Burns Clinic',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'EASY',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Partial-Thickness Forearm Burn First Aid and Dressing Management'},
    {   'content': {   'candidate_card': {   'description': 'You are an ambulatory care nurse assessing a 48-year-old '
                                                            'business consultant who returned from a 14-hour flight '
                                                            'from Singapore 3 days ago. The patient has unilateral '
                                                            'right calf swelling (calf circumference 3.5cm larger than '
                                                            'left), erythema, and deep calf tenderness.',
                                             'role': 'Nurse',
                                             'tasks': [   'Conduct a targeted clinical assessment of the affected leg '
                                                          'and check Wells score risk factors.',
                                                          'Explain what a Deep Vein Thrombosis (DVT) is in clear, '
                                                          'non-technical language.',
                                                          'Explain the urgent need for a compression Doppler '
                                                          'ultrasound scan today to confirm or rule out the clot.',
                                                          'Emphasize the risk of pulmonary embolism (PE) and teach the '
                                                          'red-flag symptoms (sudden breathlessness, sharp chest pain '
                                                          'on inspiration, hemoptysis).',
                                                          'Advise against vigorous massage of the calf.',
                                                          'Discuss potential interim anticoagulation injection if '
                                                          'ultrasound is delayed.']},
                       'patient_card': {   'description': 'You are a 48-year-old business consultant who returned from '
                                                          'a 14-hour flight from Singapore 3 days ago. Your right calf '
                                                          'is warm, aching, and swollen. You were planning to get a '
                                                          'vigorous sports massage, but your wife insisted you get '
                                                          'checked.',
                                           'tasks': [   'Explain to the nurse that your right calf has been cramping '
                                                        'and swollen since your long flight.',
                                                        'Mention that you booked a deep-tissue sports massage this '
                                                        'afternoon to work out the knot.',
                                                        'Ask whether this is just a normal muscle cramp from sitting '
                                                        'cramped in an economy seat.',
                                                        'Ask why massaging the swollen calf could be dangerous '
                                                        '(dislodging a blood clot to the lungs).',
                                                        'Ask what a Doppler ultrasound scan involves and how quickly '
                                                        'you will get the results.',
                                                        'Agree to cancel your massage, stay for the scan, and monitor '
                                                        'for any sudden chest pain.']},
                       'setting': 'Outpatient Ambulatory Care / DVT Clinic',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'MEDIUM',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Suspected Deep Vein Thrombosis (DVT) Assessment and Urgent Ultrasound Explanation'},
    {   'content': {   'candidate_card': {   'description': 'You are a nurse treating a 36-year-old jogger who was '
                                                            'bitten on the right hand and wrist by an unfamiliar '
                                                            'neighborhood dog 1 hour ago. The wound has multiple '
                                                            'puncture marks and minor lacerations.',
                                             'role': 'Nurse',
                                             'tasks': [   'Inspect the puncture wounds and check neurovascular and '
                                                          'tendon function of the fingers.',
                                                          'Explain the necessity of copious sterile saline irrigation '
                                                          'to reduce bacterial load (Pasteurella multocida).',
                                                          'Explain why puncture bite wounds on the hand are rarely '
                                                          'sutured closed (closing them traps virulent anaerobic '
                                                          'bacteria inside deep tissue spaces).',
                                                          'Check tetanus booster history (needs booster if >5 years '
                                                          'for dirty/bite wound).',
                                                          'Explain the rationale for prophylactic oral antibiotics '
                                                          '(Co-amoxiclav) and infection red flags.',
                                                          'Check understanding and arrange a 48-hour wound review.']},
                       'patient_card': {   'description': 'You are a 36-year-old jogger who was bitten on the hand by '
                                                          'an unfamiliar dog 1 hour ago. You have three puncture '
                                                          'wounds that were bleeding heavily. You want the nurse to '
                                                          "stitch the holes closed immediately so it doesn't leave a "
                                                          'scar.',
                                           'tasks': [   'Show the bleeding dog bite puncture wounds on your right hand '
                                                        'to the nurse.',
                                                        'Ask the nurse to put stitches in right away so the puncture '
                                                        'holes close up neatly.',
                                                        'Mention that your last tetanus vaccination was over 15 years '
                                                        'ago during school.',
                                                        'Ask why dog bite punctures on the hand are usually left open '
                                                        'rather than stitched closed.',
                                                        'Ask whether you need a painful rabies shot or strong '
                                                        'preventative antibiotics.',
                                                        'Agree to extensive wound flushing, a tetanus booster, and '
                                                        'oral antibiotics.']},
                       'setting': 'Minor Injuries Unit / Urgent Care',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'MEDIUM',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Dog Bite Wound Irrigation and Rabies / Tetanus Assessment'},
    {   'content': {   'candidate_card': {   'description': 'You are a community tissue viability nurse consulting '
                                                            'with a 62-year-old retired shopkeeper whose chronic '
                                                            'venous leg ulcer swab returned positive for '
                                                            'Methicillin-Resistant Staphylococcus aureus (MRSA). The '
                                                            "patient is terrified, thinking they have a 'flesh-eating "
                                                            "hospital superbug'.",
                                             'role': 'Nurse',
                                             'tasks': [   "Acknowledge the patient's anxiety and dismantle "
                                                          'sensationalized media myths about MRSA.',
                                                          "Differentiate between 'colonization' (bacteria living on "
                                                          "the surface of the wound) and 'active invasive systemic "
                                                          "infection'.",
                                                          'Reassure the patient that they are not contagious through '
                                                          'casual contact and do not need to be locked in a room at '
                                                          'home.',
                                                          'Provide practical home hygiene guidelines (regular '
                                                          'handwashing with soap, laundering personal towels/bedding '
                                                          'in warm cycle, keeping wound covered).',
                                                          'Explain the targeted topical antiseptic wash/dressing '
                                                          'protocol.',
                                                          'Check understanding and provide an MRSA information '
                                                          'leaflet.']},
                       'patient_card': {   'description': 'You are a 62-year-old patient with a chronic leg ulcer. The '
                                                          'clinic called to say your wound swab grew MRSA. You are '
                                                          'terrified, believing you caught a flesh-eating hospital '
                                                          'superbug that will require amputating your leg.',
                                           'tasks': [   'Express your intense fear to the nurse about having MRSA in '
                                                        'your chronic leg ulcer.',
                                                        'Ask whether MRSA is a flesh-eating superbug that will eat '
                                                        'through your leg bone.',
                                                        'Ask whether you can pass this superbug to your young '
                                                        'grandchildren when you hug them.',
                                                        'Ask whether you need to bleach your entire house and stay '
                                                        'isolated in a separate bedroom.',
                                                        'Listen as the nurse differentiates between surface '
                                                        'colonization and deep infection.',
                                                        'Feel reassured after learning that simple handwashing and '
                                                        'keeping the dressing intact prevents spread.']},
                       'setting': 'Community Wound Care Clinic',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'HARD',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'MRSA Colonization in Chronic Leg Ulcer: Home Isolation Precautions'},
    {   'content': {   'candidate_card': {   'description': 'You are an addictions specialist nurse assessing a '
                                                            "43-year-old accountant who decided to quit alcohol 'cold "
                                                            "turkey' 24 hours ago after drinking 10-12 units of "
                                                            'spirits daily for 4 years. The patient is exhibiting fine '
                                                            'hand tremors, diaphoresis, and marked anxiety.',
                                             'role': 'Nurse',
                                             'tasks': [   'Assess current vital signs and withdrawal severity using '
                                                          'CIWA-Ar criteria (tremor, sweating, nausea, auditory/visual '
                                                          'disturbances).',
                                                          "Commend the patient's courageous decision to seek sobriety "
                                                          'while explaining the medical danger of sudden unassisted '
                                                          'withdrawal.',
                                                          'Explain the risk of severe complications (withdrawal '
                                                          'seizures and Delirium Tremens).',
                                                          'Outline safe, medically supervised detoxification options '
                                                          '(outpatient tapering benzodiazepine regimen like '
                                                          'chlordiazepoxide, high-dose Pabrinex/thiamine).',
                                                          'Explain relapse prevention support (community keyworker, '
                                                          'group therapy, mutual aid).',
                                                          'Confirm immediate safety plan and consent for medical detox '
                                                          'pathway.']},
                       'patient_card': {   'description': 'You are a 43-year-old accountant who quit drinking cold '
                                                          'turkey 24 hours ago after years of heavy vodka consumption. '
                                                          'Your hands are shaking uncontrollably, your heart is '
                                                          'pounding, and you are sweating through your shirt.',
                                           'tasks': [   'Describe your severe hand tremors, racing heart, and sweating '
                                                        'to the addictions nurse.',
                                                        'Explain that you decided to stop drinking cold turkey '
                                                        'yesterday to save your marriage.',
                                                        'Express fear that your shaking hands will give away your '
                                                        'secret addiction to colleagues.',
                                                        'Ask why your body is shaking so violently if alcohol is '
                                                        'finally leaving your system.',
                                                        "Ask what medical detox options exist so you don't suffer a "
                                                        'seizure or delirium tremens.',
                                                        'Agree to a medically supervised outpatient detox with '
                                                        'tapering medication and vitamin B shots.']},
                       'setting': 'Community Addictions / Primary Care Assessment Clinic',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'HARD',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Alcohol Withdrawal Syndrome and Outpatient Detoxification Referral'},
    {   'content': {   'candidate_card': {   'description': 'You are a rehab nurse speaking to a proud 78-year-old '
                                                            'retired school headmistress on Day 5 following surgical '
                                                            'repair of a fractured neck of femur. The patient was '
                                                            'found walking across the ward unassisted without her '
                                                            'prescribed 4-wheeled walker.',
                                             'role': 'Nurse',
                                             'tasks': [   'Approach the patient respectfully, preserving her dignity '
                                                          'and autonomy.',
                                                          'Explore her reasons for not using the 4-wheeled walking '
                                                          'frame.',
                                                          "Acknowledge her fear of looking 'frail and old' in front of "
                                                          'other residents.',
                                                          'Explain the biomechanical purpose of the walking frame '
                                                          '(providing base of support, preventing catastrophic '
                                                          're-fracture or fall).',
                                                          'Discuss home environmental hazards (loose rugs, bathroom '
                                                          'grab rails, non-slip footwear, adequate lighting).',
                                                          'Agree on a mutual safety contract: calling for nurse '
                                                          'assistance when mobilizing until cleared by the '
                                                          'physiotherapist.']},
                       'patient_card': {   'description': 'You are a 78-year-old retired headmistress on Day 5 after '
                                                          'surgery for a broken hip. The nurse caught you walking '
                                                          'without your prescribed 4-wheeled walker. You feel '
                                                          'humiliated by the walker and refuse to look like a frail '
                                                          'invalid.',
                                           'tasks': [   'Defend walking without your frame, stating you have walked on '
                                                        'your own feet for 78 years.',
                                                        'Express how humiliating that bulky metal trolley feels in '
                                                        'front of other ward patients.',
                                                        'Ask why you cannot just hold onto furniture or walls to get '
                                                        'to the bathroom.',
                                                        'Ask whether you will be stuck using a walking frame for the '
                                                        'rest of your life.',
                                                        'Ask what home hazards (loose rugs, dim lighting) cause '
                                                        'elderly people to re-fracture hips.',
                                                        'Agree to use the walker temporarily as your quickest passport '
                                                        'to being discharged home safely.']},
                       'setting': 'Sub-Acute Geriatric Rehabilitation Ward',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'MEDIUM',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Aged Care Fall Prevention and Mobility Aid Compliance'},
    {   'content': {   'candidate_card': {   'description': 'You are a dementia specialist nurse consulting with an '
                                                            'exhausted 55-year-old daughter who is the sole caregiver '
                                                            "for her 81-year-old mother with progressive Alzheimer's "
                                                            'disease. The mother was recently found wandering down a '
                                                            'busy street in her nightgown at 2:00 AM.',
                                             'role': 'Nurse',
                                             'tasks': [   "Demonstrate deep empathy for the daughter's overwhelming "
                                                          'caregiver burden and exhaustion.',
                                                          'Validate her feelings of guilt, grief, and burnout.',
                                                          'Explain wandering behaviors in dementia (disorientation to '
                                                          "time, searching for familiar past routines like 'going to "
                                                          "work').",
                                                          'Recommend practical safety interventions (door alarms, '
                                                          'wearable GPS tracking pendant, hidden door locks, '
                                                          'dementia-friendly night lighting).',
                                                          'Discuss formal respite care services (day care centres, '
                                                          'short-term residential respite, home care packages).',
                                                          'Encourage carer self-care and provide Carers UK / '
                                                          "Alzheimer's Society support contacts."]},
                       'patient_card': {   'description': 'You are the 55-year-old daughter and sole caregiver for '
                                                          "your 81-year-old mother with Alzheimer's disease. Last "
                                                          'night the police brought her home at 2:30 AM after finding '
                                                          'her wandering the streets in her slippers. You are breaking '
                                                          'down from exhaustion and guilt.',
                                           'tasks': [   'Break down in tears and describe the terrifying moment the '
                                                        'police brought your mother home.',
                                                        'Describe your physical and emotional exhaustion from barely '
                                                        'sleeping for months.',
                                                        'Express your guilt that you feel resentful and wish you could '
                                                        'have a break from caregiving.',
                                                        'Ask what safety measures (door alarms, GPS trackers, modified '
                                                        'door locks) stop night wandering.',
                                                        'Ask how respite care works and whether your mother will feel '
                                                        'abandoned in day care.',
                                                        'Accept referrals for carer support groups and arrange a trial '
                                                        'day of respite care.']},
                       'setting': 'Memory Assessment and Community Dementia Service',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'HARD',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Early-Stage Dementia: Carer Burnout and Wandering Safety'},
    {   'content': {   'candidate_card': {   'description': 'You are caring for an 83-year-old stroke patient with '
                                                            'left-sided hemiplegia who has developed Stage 1 '
                                                            'non-blanching erythema over the sacrum. The patient '
                                                            "complains that the nurses' two-hourly turning schedule "
                                                            'wakes them up and insists on sleeping flat on their back.',
                                             'role': 'Nurse',
                                             'tasks': [   'Greet the patient kindly and assess their current comfort '
                                                          'and skin condition.',
                                                          'Explain what a pressure ulcer (bedsore) is and how '
                                                          'continuous pressure stops capillary blood flow to the skin.',
                                                          'Explain the importance of the 30-degree tilt two-hourly '
                                                          'repositioning schedule.',
                                                          'Demonstrate pressure-relieving aids (alternating pressure '
                                                          'air mattress, heel protector boots, barrier cream).',
                                                          'Discuss the critical role of nutrition and hydration '
                                                          '(protein intake for tissue integrity).',
                                                          'Establish a mutually agreeable turning routine that '
                                                          'minimizes sleep disruption.']},
                       'patient_card': {   'description': 'You are an 83-year-old patient recovering from a stroke. '
                                                          'The nurses keep waking you every two hours to turn you on '
                                                          'your side because of a red spot on your tailbone. You are '
                                                          'irritable from broken sleep and want to sleep flat on your '
                                                          'back.',
                                           'tasks': [   'Complain to the nurse that two-hourly turning is ruining your '
                                                        'sleep and making you exhausted.',
                                                        'Dismiss the red spot on your tailbone as just a minor skin '
                                                        'irritation that will heal on its own.',
                                                        'Ask why lying flat in a comfortable hospital bed causes skin '
                                                        'to break down into ulcers.',
                                                        'Ask whether an alternating pressure air mattress can reduce '
                                                        'the need for turning at night.',
                                                        'Ask why nutrition and hydration are important for keeping '
                                                        'your skin intact.',
                                                        'Agree to a 30-degree tilt turning schedule with pillow '
                                                        'support to protect your tailbone.']},
                       'setting': 'Sub-Acute Medical Inpatient Unit',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'MEDIUM',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Pressure Injury Prevention and Repositioning in Immobile Patient'},
    {   'content': {   'candidate_card': {   'description': 'You are a stroke rehabilitation nurse delivering a '
                                                            'lunchtime tray to a 71-year-old patient who suffered an '
                                                            'acute middle cerebral artery stroke 1 week ago. The '
                                                            'speech therapist recommended Level 2 mildly thick fluids, '
                                                            'but the patient is angry that their cup of English tea is '
                                                            "thick and demands 'normal' water.",
                                             'role': 'Nurse',
                                             'tasks': [   "Acknowledge the patient's frustration with modified "
                                                          'thickened fluids with warmth and tact.',
                                                          'Explain the mechanism of dysphagia (swallowing nerve '
                                                          'impairment causing fluids to slip into the '
                                                          'trachea/windpipe).',
                                                          "Explain the serious danger of 'silent aspiration' and "
                                                          'aspiration pneumonia.',
                                                          'Demonstrate safe swallowing techniques (sitting upright at '
                                                          '90 degrees, chin-tuck posture, small single sips, remaining '
                                                          'upright for 30 minutes after meals).',
                                                          'Discuss ongoing speech therapy assessments and the goal of '
                                                          'returning to thin fluids as throat muscles strengthen.',
                                                          'Offer temperature/flavor adjustments for thickened fluids '
                                                          'to make them more palatable.']},
                       'patient_card': {   'description': 'You are a 71-year-old stroke patient who had difficulty '
                                                          'swallowing on a bedside test. The nurse delivers your lunch '
                                                          'with thick, gelatinous tea. You are disgusted, insulted, '
                                                          'and demand a normal cup of thin hot tea and water.',
                                           'tasks': [   'Complain angrily that your cup of tea looks like wallpaper '
                                                        'paste and tastes unnatural.',
                                                        'Demand a normal glass of cold water, claiming you have '
                                                        'swallowed normally for 71 years.',
                                                        'Ask what silent aspiration is and why thin liquids are '
                                                        'dangerous for recovering stroke patients.',
                                                        'Ask how long you will have to endure thickened fluids and '
                                                        'pureed soft food.',
                                                        'Ask what swallowing exercises and head postures (chin-tuck) '
                                                        'make swallowing safer.',
                                                        "Reluctantly agree to follow the speech therapist's thickened "
                                                        'fluid plan until your next reassessment.']},
                       'setting': 'Stroke Rehabilitation Unit',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'MEDIUM',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Stroke Rehabilitation: Dysphagia Precautions and Thickened Fluids'},
    {   'content': {   'candidate_card': {   'description': "You are a Parkinson's specialist nurse consulting with a "
                                                            '67-year-old retired civil engineer with a 6-year history '
                                                            "of Parkinson's disease. The patient reports unpredictable "
                                                            "episodes where his body 'freezes like concrete' in "
                                                            'supermarket aisles, despite taking Co-careldopa '
                                                            '(Sinemet).',
                                             'role': 'Nurse',
                                             'tasks': [   "Explore the patient's medication schedule and specific "
                                                          "timing of 'freezing' or motor fluctuations.",
                                                          "Explain the 'On-Off' phenomenon and medication wear-off as "
                                                          "Parkinson's progresses.",
                                                          'Emphasize the crucial importance of exact, timely dosing '
                                                          "(taking Levodopa at the exact clock hour, not 'around "
                                                          "breakfast/lunch').",
                                                          'Explain food-drug interactions: high-protein meals compete '
                                                          'with Levodopa for absorption across the blood-brain barrier '
                                                          '(advise taking medication 30-45 minutes before meals or '
                                                          'adjusting protein to evening).',
                                                          "Introduce a symptom diary to track 'on' and 'off' periods "
                                                          'before consulting the neurologist for dose adjustments.',
                                                          'Provide practical cueing strategies to break freezing '
                                                          'episodes (stepping over an imaginary line, rhythmic '
                                                          'counting).']},
                       'patient_card': {   'description': "You are a 67-year-old retired engineer with Parkinson's "
                                                          "disease. Recently your legs have been 'freezing' completely "
                                                          'to the floor in public places. You take your Sinemet pills '
                                                          'whenever you remember, often right after a heavy bacon and '
                                                          'egg breakfast.',
                                           'tasks': [   'Describe the terrifying freezing episodes where your feet '
                                                        'feel glued to the supermarket floor.',
                                                        'Admit that you take your Sinemet doses irregularly and often '
                                                        'eat heavy protein breakfasts.',
                                                        "Ask why your Parkinson's medication works well for two hours "
                                                        'and then abruptly stops working.',
                                                        'Ask why eating high-protein meals interferes with how '
                                                        'Levodopa enters the brain.',
                                                        'Ask what rhythmic cueing techniques can help unfreeze your '
                                                        'feet when stuck in public.',
                                                        'Agree to take your medication exactly 30 minutes before meals '
                                                        'and keep a timed symptom diary.']},
                       'setting': 'Movement Disorders Neurology Clinic',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'HARD',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': "Parkinson's Disease: Critical Timing of Levodopa and 'On-Off' Phenomenon"},
    {   'content': {   'candidate_card': {   'description': 'You are a bone health clinical nurse reviewing the DEXA '
                                                            'scan results of a 63-year-old postmenopausal woman. Her '
                                                            'lumbar spine T-score is -2.8, confirming osteoporosis. '
                                                            "The patient is anxious that her bones are 'crumbling' and "
                                                            'thinks she must stop all physical exercise.',
                                             'role': 'Nurse',
                                             'tasks': [   'Welcome the patient and explain what a DEXA T-score of -2.8 '
                                                          'means in accessible language.',
                                                          "Reassure her that her bones are not 'crumbling' and that "
                                                          'osteoporosis is manageable and treatable.',
                                                          'Emphasize the vital benefits of weight-bearing and '
                                                          'resistance exercise (walking, brisk marching, light '
                                                          'weights) in stimulating bone remodeling.',
                                                          'Review dietary sources of Calcium (dairy, fortified plant '
                                                          'milks, leafy greens, canned sardines with bones) aiming for '
                                                          '1200mg daily.',
                                                          'Explain the importance of Vitamin D (sunlight exposure and '
                                                          '800-1000 IU daily supplementation) for calcium absorption.',
                                                          'Discuss home fall-prevention measures and outline upcoming '
                                                          'medical treatments (bisphosphonates).']},
                       'patient_card': {   'description': 'You are a 63-year-old woman whose DEXA bone scan showed '
                                                          'osteoporosis (T-score -2.8). Your mother suffered a '
                                                          'catastrophic hip fracture, so you are terrified your bones '
                                                          'are crumbling and believe you must stop all gardening and '
                                                          'walking.',
                                           'tasks': [   'Express your panic to the nurse that your bones are crumbling '
                                                        'and you could snap your spine.',
                                                        "Describe your mother's hip fracture and your terror of ending "
                                                        'up bedbound like her.',
                                                        'Ask whether bending over to garden or walking briskly is '
                                                        'dangerous for fragile bones.',
                                                        'Ask how much dietary calcium and Vitamin D you need daily, '
                                                        "especially since you don't eat dairy.",
                                                        'Ask how prescription bone medications (bisphosphonates) '
                                                        'strengthen existing bone density.',
                                                        'Re-engage enthusiastically with daily weight-bearing walking '
                                                        'and take prescribed supplements.']},
                       'setting': 'Bone Health and Rheumatology Outpatient Service',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'EASY',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Osteoporosis: Bone Density T-Score and Calcium / Vitamin D Lifestyle'},
    {   'content': {   'candidate_card': {   'description': 'You are a continence nurse specialist consulting with a '
                                                            '45-year-old mother of three who is experiencing stress '
                                                            'urinary incontinence when coughing, sneezing, or jogging. '
                                                            'She is deeply embarrassed, wears thick menstrual pads '
                                                            'daily, and has stopped going to her fitness classes.',
                                             'role': 'Nurse',
                                             'tasks': [   'Provide a safe, empathetic, and confidential environment to '
                                                          'normalize stress incontinence.',
                                                          'Explain the anatomy and mechanics of the pelvic floor '
                                                          'muscles supporting the bladder neck.',
                                                          'Provide clear instructions for Pelvic Floor Muscle Training '
                                                          '(Kegel exercises: slow sustained contractions for 10 '
                                                          'seconds followed by quick flick contractions, 3 sets '
                                                          'daily).',
                                                          'Discuss bladder irritants (caffeine, carbonated drinks, '
                                                          'artificial sweeteners, alcohol) that worsen urgency.',
                                                          'Explain bladder retraining techniques (timed voiding, '
                                                          'deferral strategies).',
                                                          'Provide encouraging long-term expectations (improvement '
                                                          'seen within 8-12 weeks of consistent daily exercises).']},
                       'patient_card': {   'description': 'You are a 45-year-old mother of three who leaks urine '
                                                          'whenever you sneeze, laugh, or try to jog. You wear bulky '
                                                          'sanitary pads daily, feel humiliated, and stopped attending '
                                                          'your weekly fitness classes.',
                                           'tasks': [   'Confide in the continence nurse with embarrassment about '
                                                        'leaking urine during coughing or exercise.',
                                                        'Describe how this stress incontinence forced you to quit your '
                                                        'running group and gym workouts.',
                                                        'Ask whether surgery is the only cure or if pelvic floor '
                                                        'exercises can genuinely restore control.',
                                                        'Ask how to perform pelvic floor (Kegel) squeezes correctly '
                                                        'without tensing your stomach.',
                                                        'Ask why drinking 4 to 5 cups of coffee daily makes bladder '
                                                        'leakage and urgency worse.',
                                                        'Commit to performing three sets of daily pelvic floor muscle '
                                                        'exercises for the next 12 weeks.']},
                       'setting': "Women's Health / Continence Clinic",
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'MEDIUM',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Urinary Incontinence: Pelvic Floor Exercises and Bladder Retraining'},
    {   'content': {   'candidate_card': {   'description': 'You are an aged care clinical nurse conducting annual '
                                                            'influenza immunization rounds for facility residents. An '
                                                            '80-year-old resident is refusing the flu vaccine, '
                                                            "claiming 'the jab gave me the worst flu of my life three "
                                                            "years ago.'",
                                             'role': 'Nurse',
                                             'tasks': [   "Listen respectfully to the resident's past negative "
                                                          'experience and validate their feelings.',
                                                          'Explain the biological science of the vaccine: it contains '
                                                          'inactivated (killed) virus particles and CANNOT cause the '
                                                          'flu.',
                                                          'Differentiate between normal immune response (mild '
                                                          'soreness, low-grade fever for 24-48 hours) and actual '
                                                          'influenza infection.',
                                                          'Explain the high vulnerability of aged care residents to '
                                                          'severe influenza complications (pneumonia, hospitalization, '
                                                          'heart stress).',
                                                          'Discuss community cocooning / herd protection for fellow '
                                                          'frail residents.',
                                                          "Respect the resident's ultimate right to choose while "
                                                          'offering reassurance.']},
                       'patient_card': {   'description': 'You are an 80-year-old resident in an aged care home. The '
                                                          'clinical nurse is offering the annual influenza vaccine. '
                                                          'You adamantly refuse, claiming that the shot gave you the '
                                                          'worst flu of your life three years ago.',
                                           'tasks': [   'Refuse the flu vaccine firmly, telling the nurse that the '
                                                        'injection gives people the actual flu.',
                                                        'Describe how sick, achy, and feverish you felt for two days '
                                                        'after a previous flu jab.',
                                                        'Ask why the government injects live flu viruses into elderly '
                                                        'residents.',
                                                        'Ask whether practicing good handwashing and taking vitamin C '
                                                        'can protect you just as well.',
                                                        'Listen as the nurse explains that the vaccine is made from '
                                                        'killed, inactive virus fragments.',
                                                        'Reconsider and agree to have the vaccine to protect yourself '
                                                        'and frail friends in the home.']},
                       'setting': 'Residential Aged Care Facility',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'MEDIUM',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Influenza Vaccination Hesitancy in Residential Aged Care'},
    {   'content': {   'candidate_card': {   'description': 'You are an oncology nurse consulting with a 52-year-old '
                                                            'woman undergoing her second cycle of adjuvant '
                                                            'chemotherapy for breast cancer. The patient reports '
                                                            'severe nausea, metallic taste in the mouth, and '
                                                            'significant weight loss.',
                                             'role': 'Nurse',
                                             'tasks': [   'Assess the severity, timing, and pattern of nausea '
                                                          '(anticipatory vs. acute vs. delayed).',
                                                          'Review her current anti-emetic schedule and emphasize '
                                                          'prophylactic timing (taking anti-emetics regularly as '
                                                          'prescribed, not waiting until vomiting starts).',
                                                          'Provide practical nutritional strategies (small, frequent '
                                                          'cool/room-temperature meals, ginger tea, dry crackers '
                                                          'before rising).',
                                                          'Address taste alterations (using plastic or wooden cutlery '
                                                          'to prevent metallic taste, marinating proteins, lemon '
                                                          'water).',
                                                          'Emphasize adequate hydration and recognize dehydration red '
                                                          'flags.',
                                                          'Coordinate with the oncologist for medication optimization '
                                                          '(adding Aprepitant or Dexamethasone).']},
                       'patient_card': {   'description': 'You are a 52-year-old woman receiving chemotherapy for '
                                                          'breast cancer. You suffer from severe waves of nausea, a '
                                                          'disgusting metallic taste in your mouth, and weight loss. '
                                                          'You only take your anti-nausea pills once vomiting has '
                                                          'already started.',
                                           'tasks': [   'Describe the overwhelming nausea and retching you experience '
                                                        'after chemotherapy sessions.',
                                                        'Complain that all food tastes like sucking on rusty coins, '
                                                        'causing you to lose 3 kg.',
                                                        'Admit that you only take your anti-emetic tablets after you '
                                                        'already feel violently ill.',
                                                        'Ask why taking anti-nausea pills after vomiting starts is '
                                                        'much less effective than taking them before.',
                                                        'Ask what eating tricks (plastic cutlery, cold foods, ginger '
                                                        'tea) stop the metallic taste.',
                                                        'Agree to take your anti-emetic medications on a strict clock '
                                                        'schedule before nausea sets in.']},
                       'setting': 'Day Oncology Chemotherapy Infusion Unit',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'MEDIUM',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Chemotherapy-Induced Nausea and Nutritional Support Strategies'},
    {   'content': {   'candidate_card': {   'description': 'You are a palliative care nurse speaking to the '
                                                            '58-year-old son of a 84-year-old patient with end-stage '
                                                            'metastatic pancreatic cancer. The medical team has '
                                                            'recommended setting up a subcutaneous syringe driver with '
                                                            'Diamorphine/Midazolam for intractable pain and '
                                                            'restlessness, but the son is adamantly opposed.',
                                             'role': 'Nurse',
                                             'tasks': [   'Approach the son with profound compassion, active '
                                                          'listening, and unhurried emotional presence.',
                                                          'Acknowledge and explore his fear that starting a syringe '
                                                          "driver will hasten his father's death (euthanasia myth).",
                                                          'Explain the therapeutic purpose of the continuous '
                                                          'subcutaneous syringe driver (delivering steady, low-dose '
                                                          'pain and symptom relief when oral route fails).',
                                                          'Differentiate between providing palliative comfort and '
                                                          'hastening death (doctrine of double effect; goal is quality '
                                                          'of comfort, not ending life).',
                                                          'Reassure him that breakthrough doses are calibrated to '
                                                          'comfort, not sedation.',
                                                          "Invite the son to participate in his father's comfort care "
                                                          '(moistening lips, holding hands, quiet presence).']},
                       'patient_card': {   'description': 'You are the 58-year-old son of a dying cancer patient in '
                                                          'hospice. The palliative team wants to start a continuous '
                                                          'subcutaneous morphine syringe driver for pain. You are '
                                                          'furious, believing the morphine pump is euthanasia designed '
                                                          'to hasten his death.',
                                           'tasks': [   'Accuse the hospice team of using the morphine pump to speed '
                                                        "up your father's death.",
                                                        'Describe how terrified you are that morphine will shut down '
                                                        'his breathing within hours.',
                                                        'Ask whether starting a continuous syringe driver means the '
                                                        'medical team is giving up on him.',
                                                        'Ask how steady low-dose morphine eases pain and '
                                                        'breathlessness without shortening life.',
                                                        'Ask whether your father will still be able to hear your voice '
                                                        'and feel your hand.',
                                                        'Tearfully give consent for the syringe driver once the nurse '
                                                        'reassures you of his comfort.']},
                       'setting': 'Palliative Inpatient Hospice',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'HARD',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Palliative Care: Subcutaneous Syringe Driver and Morphine Myths'},
    {   'content': {   'candidate_card': {   'description': 'You are a community palliative care clinical nurse '
                                                            'specialist visiting the home of a 62-year-old husband '
                                                            'caring full-time for his 59-year-old wife with advanced '
                                                            'Amyotrophic Lateral Sclerosis (Motor Neurone Disease). '
                                                            'The husband is physically and emotionally breaking down.',
                                             'role': 'Nurse',
                                             'tasks': [   'Acknowledge the immense love, dedication, and heavy '
                                                          'physical burden the husband is carrying.',
                                                          "Assess the caregiver's physical and mental health (sleep, "
                                                          'nutrition, isolation, anxiety).',
                                                          'Normalize the need for rest and dismantle his guilt about '
                                                          'needing outside help.',
                                                          'Explain available support options: night-sitting services, '
                                                          'Marie Curie / Macmillan nursing visits, short-term '
                                                          'inpatient hospice respite.',
                                                          'Explain that accepting respite care ensures he can remain '
                                                          'healthy enough to continue loving and supporting his wife.',
                                                          'Create a step-by-step plan to initiate community respite '
                                                          'services collaboratively.']},
                       'patient_card': {   'description': 'You are a 62-year-old husband caring full-time for your '
                                                          "bedbound wife with advanced ALS/MND. You haven't left the "
                                                          'house in three weeks, have severe back pain from manual '
                                                          'lifting, and are weeping with exhaustion, but you feel '
                                                          'guilty about seeking respite.',
                                           'tasks': [   'Confide tearfully in the palliative nurse that you are '
                                                        'breaking down under the 24/7 care burden.',
                                                        'Describe your physical back pain and insomnia from turning '
                                                        'and suctioning your wife all night.',
                                                        'Express deep guilt that accepting respite care feels like '
                                                        'breaking your marriage wedding vows.',
                                                        'Ask what respite options exist (inpatient hospice stay, '
                                                        'night-sitting nurses in your home).',
                                                        'Ask whether respite staff can properly manage her complex '
                                                        'feeding tube and suction machine.',
                                                        'Accept a week of hospice respite care so you can rest and '
                                                        'regain strength to continue caring for her.']},
                       'setting': 'Community Palliative Care Home Visit',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'HARD',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Palliative Home Care: Carer Burnout and Respite Services'},
    {   'content': {   'candidate_card': {   'description': 'You are a stomal therapy nurse seeing a 56-year-old '
                                                            "patient who underwent an emergency Hartmann's procedure "
                                                            'with permanent end colostomy 4 weeks ago. The patient is '
                                                            'distressed because their stoma pouch leaked in a café '
                                                            'yesterday, and they now refuse to leave their house.',
                                             'role': 'Nurse',
                                             'tasks': [   "Validate the patient's acute embarrassment and "
                                                          'psychological trauma from the public pouch leak.',
                                                          'Inspect the peristomal skin, stoma size, and current '
                                                          'appliance fit.',
                                                          'Troubleshoot the leakage cause (changes in stoma size as '
                                                          'post-op swelling resolves, needing a custom flange or '
                                                          'convex wafer).',
                                                          'Demonstrate proper stoma pouch application (measuring stoma '
                                                          'diameter, warm hand seal, barrier paste/rings).',
                                                          'Address odor fears with evidence-based solutions (charcoal '
                                                          'filters in modern bags, lubricating deodorant drops).',
                                                          'Offer peer support through ostomy associations and check '
                                                          'understanding.']},
                       'patient_card': {   'description': 'You are a 56-year-old patient with a new colostomy. '
                                                          'Yesterday your stoma pouch leaked stool down your trousers '
                                                          'in a crowded café. You threw your clothes away and are so '
                                                          'mortified that you swear you will never leave your home '
                                                          'again.',
                                           'tasks': [   'Describe the devastating public humiliation you suffered when '
                                                        'your stoma pouch leaked in a café.',
                                                        'Express your intense fear that people around you can smell '
                                                        'fecal odor from your stoma.',
                                                        'Vow to the stoma nurse that you will never go back to work or '
                                                        'leave your house again.',
                                                        'Ask why the bag leaked and whether stoma shrinkage after '
                                                        'surgery created a loose seal.',
                                                        'Ask what modern deodorizing drops and charcoal filters '
                                                        'prevent odor from escaping.',
                                                        'Learn how to measure and cut the baseplate accurately and '
                                                        'regain confidence to go out.']},
                       'setting': 'Stoma Care Outpatient Clinic',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'MEDIUM',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Colostomy Stoma Care and Overcoming Pouch Leakage and Odor Anxiety'},
    {   'content': {   'candidate_card': {   'description': 'You are a community health visitor / maternal health '
                                                            'nurse conducting a routine 6-week postnatal home check '
                                                            'for a 31-year-old mother. Her Edinburgh Postnatal '
                                                            'Depression Scale (EPDS) score is 16/30. She is tearful, '
                                                            'anxious, experiencing intrusive thoughts of inadequacy, '
                                                            'and terrified social services will take her baby.',
                                             'role': 'Nurse',
                                             'tasks': [   'Establish a safe, non-judgmental, compassionate '
                                                          'environment.',
                                                          'Discuss the EPDS score gently, normalizing postnatal '
                                                          'depression as a common medical condition affecting 1 in 7 '
                                                          'mothers.',
                                                          'Directly address and dismantle her fear of social services '
                                                          '(clarify that asking for help proves she is a caring, '
                                                          'loving mother and support is designed to keep families '
                                                          'together).',
                                                          'Differentiate between normal maternal fatigue and clinical '
                                                          'postnatal depression.',
                                                          'Outline effective support pathways (GP consultation, '
                                                          'talking therapies/CBT, mother-and-baby mental health teams, '
                                                          'safe breastfeeding-compatible SSRIs).',
                                                          'Establish an immediate safety and support network with her '
                                                          'partner/family, and arrange a follow-up visit.']},
                       'patient_card': {   'description': 'You are a 31-year-old mother of a 6-week-old baby. You '
                                                          'scored 16 on the postnatal depression screening tool. You '
                                                          'feel numb, weep constantly, and have intrusive thoughts of '
                                                          'inadequacy, but you are terrified social services will take '
                                                          'your baby.',
                                           'tasks': [   'Break down in tears and ask the health visitor not to judge '
                                                        'your depression screening score.',
                                                        'Express your terror that admitting you are depressed will '
                                                        'cause social services to take your baby.',
                                                        'Describe how detached, exhausted, and guilty you feel despite '
                                                        'loving your newborn son.',
                                                        'Ask whether postnatal depression is a genuine medical '
                                                        'condition or a sign you are a bad mother.',
                                                        'Ask whether taking antidepressant medication is safe while '
                                                        'continuing to breastfeed.',
                                                        'Accept support from the community perinatal mental health '
                                                        'team and involve your partner.']},
                       'setting': 'Community Maternal and Child Health Home Visit',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'HARD',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Postnatal Depression: Screening, Stigma, and Community Health Support'},
    {   'content': {   'candidate_card': {   'description': 'You are a tuberculosis specialist nurse seeing a '
                                                            '34-year-old restaurant employee undergoing treatment for '
                                                            'active pulmonary TB. After completing 2 months of '
                                                            'quadruple therapy (Rifater/Ethambutol), the patient feels '
                                                            'healthy and wants to stop taking the medications because '
                                                            'of reddish-orange urine.',
                                             'role': 'Nurse',
                                             'tasks': [   "Acknowledge the patient's positive clinical recovery "
                                                          '(weight gain, resolution of cough and night sweats).',
                                                          'Explain why TB bacteria require a full 6-month continuous '
                                                          'course (dormant bacteria remain hidden in tubercles; '
                                                          'stopping early causes multidrug-resistant TB - MDR-TB).',
                                                          'Reassure the patient regarding reddish-orange discoloration '
                                                          'of urine, tears, and sweat (harmless side effect of '
                                                          'Rifampicin).',
                                                          'Explain the serious consequences of drug-resistant TB '
                                                          '(years of second-line toxic injections, potential relapse).',
                                                          'Discuss liver monitoring and avoiding alcohol during the '
                                                          'continuation phase (Isoniazid and Rifampicin).',
                                                          'Reinforce adherence with a medication tracker and check '
                                                          'understanding.']},
                       'patient_card': {   'description': 'You are a 34-year-old patient who completed 2 months of '
                                                          'intensive quadruple antibiotics for active pulmonary '
                                                          'tuberculosis. Your cough has vanished and you feel great. '
                                                          'You want to stop taking the pills because they turn your '
                                                          'urine bright reddish-orange.',
                                           'tasks': [   'Tell the TB nurse happily that you feel 100% cured and want '
                                                        'to stop taking your daily pills.',
                                                        'Express alarm that the medication is turning your urine, '
                                                        'sweat, and saliva bright orange.',
                                                        'Ask why you need four more months of antibiotics if your '
                                                        'cough and fever are completely gone.',
                                                        'Ask what multidrug-resistant tuberculosis (MDR-TB) is and '
                                                        'what happens if you stop pills early.',
                                                        'Ask whether the orange urine indicates permanent liver or '
                                                        'kidney damage from the drugs.',
                                                        'Agree to complete the remaining 4-month continuation phase of '
                                                        'Isoniazid and Rifampicin.']},
                       'setting': 'Public Health Respiratory and TB Clinic',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'HARD',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Tuberculosis: Directly Observed Therapy (DOT) and Completing 6-Month Course'},
    {   'content': {   'candidate_card': {   'description': 'You are a practice nurse dressing a painful vesicular '
                                                            'unilateral dermatomal rash on the right thoracic ribcage '
                                                            'of a 66-year-old grandmother. The GP diagnosed Herpes '
                                                            'Zoster (Shingles) and prescribed oral Aciclovir. The '
                                                            'patient plans to babysit her 6-month-old unvaccinated '
                                                            'grandson tomorrow.',
                                             'role': 'Nurse',
                                             'tasks': [   "Assess the patient's pain level and examine the vesicular "
                                                          'rash.',
                                                          'Explain the pathogenesis of shingles (reactivation of '
                                                          'dormant chickenpox virus along a nerve pathway).',
                                                          'Explain transmission risks: shingles cannot be caught '
                                                          'directly as shingles, but blister fluid CAN transmit '
                                                          'chickenpox to non-immune individuals.',
                                                          'Advise against contact with high-risk vulnerable groups '
                                                          '(unvaccinated infants, pregnant women, immunocompromised '
                                                          'individuals) until all blisters have fully crusted over.',
                                                          'Discuss wound care (keeping rash loosely covered with '
                                                          'non-stick dressing, avoiding burst blisters or antibiotic '
                                                          'creams).',
                                                          'Review Aciclovir compliance (completing 7-day course) and '
                                                          'post-herpetic neuralgia monitoring.']},
                       'patient_card': {   'description': 'You are a 66-year-old grandmother with a painful shingles '
                                                          'rash on your right ribs. The doctor prescribed Aciclovir. '
                                                          'You are planning to babysit your 6-month-old unvaccinated '
                                                          'grandson tomorrow and want the nurse to put a bandage over '
                                                          'the blisters.',
                                           'tasks': [   'Explain your burning rib rash to the practice nurse and ask '
                                                        'for a quick dressing.',
                                                        'Mention that you need to babysit your 6-month-old grandson '
                                                        'tomorrow while your daughter works.',
                                                        'Express surprise when the nurse warns that your blister fluid '
                                                        'can transmit chickenpox.',
                                                        'Ask how long the blisters remain contagious to infants and '
                                                        'pregnant women.',
                                                        'Ask how to care for the rash at home without popping blisters '
                                                        'or causing secondary infection.',
                                                        'Agree to cancel babysitting until every blister has '
                                                        'completely crusted over.']},
                       'setting': 'Primary Care / General Practice Clinic',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'EASY',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Shingles (Herpes Zoster): Rash Care, Antivirals, and Transmission Safety'},
    {   'content': {   'candidate_card': {   'description': 'You are a practice nurse seeing a 54-year-old sales '
                                                            'executive presenting with an acutely inflamed, '
                                                            'exquisitely painful, swollen first metatarsophalangeal '
                                                            'joint (left big toe). The patient was prescribed '
                                                            'Colchicine and Naproxen by the triage doctor, but is '
                                                            'confused about triggers and long-term prevention.',
                                             'role': 'Nurse',
                                             'tasks': [   'Acknowledge the extreme sensitivity and pain of acute gouty '
                                                          'arthritis.',
                                                          'Explain the pathology of gout (uric acid crystals '
                                                          'depositing in the joint space due to hyperuricemia).',
                                                          'Clarify medication instructions (Colchicine for acute '
                                                          'attack; stop if diarrhea develops; take Naproxen with food '
                                                          'or omeprazole).',
                                                          'Identify dietary purine triggers (beer/stout, spirits, red '
                                                          'meat, organ meats, shellfish, high-fructose corn syrup).',
                                                          'Recommend positive lifestyle interventions (drinking 2-3 '
                                                          'litres of water daily to flush uric acid, low-fat dairy, '
                                                          'cherry extract).',
                                                          'Explain that long-term preventive medication (Allopurinol) '
                                                          'is started only after the acute flare resolves.']},
                       'patient_card': {   'description': 'You are a 54-year-old sales executive suffering an '
                                                          'excruciating attack of acute gout in your left big toe '
                                                          '(9/10 pain) after barbecue ribs and beer. You cannot bear '
                                                          'even a bedsheet touching your toe and want immediate '
                                                          'relief.',
                                           'tasks': [   'Beg the nurse not to touch your foot because the throbbing '
                                                        'pain in your big toe is a 9/10.',
                                                        'Describe how the agony flared up overnight following a feast '
                                                        'of red meat and craft beer.',
                                                        'Ask why dietary purines in beer, steaks, and shellfish '
                                                        'trigger uric acid crystals in the joint.',
                                                        'Ask how to take Colchicine and Naproxen safely without '
                                                        'getting severe stomach upset.',
                                                        'Ask why long-term preventive medication (Allopurinol) cannot '
                                                        'be started during an acute flare.',
                                                        'Agree to drink 2 to 3 litres of water daily, reduce beer '
                                                        'consumption, and rest the elevated foot.']},
                       'setting': 'Urgent Care Primary Care Centre',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'EASY',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Acute Gout Attack: Colchicine vs. NSAIDs and Dietary Purine Triggers'},
    {   'content': {   'candidate_card': {   'description': 'You are an infection prevention and control nurse '
                                                            'speaking to a 74-year-old inpatient recovering from '
                                                            'Clostridioides difficile (C. diff) infection following '
                                                            'broad-spectrum antibiotics for pneumonia. The patient is '
                                                            'using alcohol hand gel rather than soap and water and is '
                                                            'upset about being in an isolation side-room.',
                                             'role': 'Nurse',
                                             'tasks': [   'Acknowledge the psychological loneliness and frustration of '
                                                          'contact isolation.',
                                                          'Explain how C. diff spores develop (antibiotics disrupt '
                                                          'normal protective gut flora, allowing C. diff to '
                                                          'proliferate).',
                                                          'Crucial clinical teaching: explain why alcohol hand rub is '
                                                          'INEFFECTIVE against C. diff (spores have a hard protective '
                                                          'shell that only mechanical friction with soap and running '
                                                          'water can wash away).',
                                                          'Explain contact precautions (PPE for staff, dedicated '
                                                          'commode, bleach-based environmental cleaning).',
                                                          'Discuss the treatment course (oral Vancomycin) and signs of '
                                                          'clinical recovery.',
                                                          'Clarify criteria for discontinuing isolation (48 hours free '
                                                          'of diarrhea with formed stool).']},
                       'patient_card': {   'description': 'You are a 74-year-old patient in hospital isolation '
                                                          'recovering from Clostridioides difficile diarrhea. You feel '
                                                          'lonely and resentful about contact precautions, and you '
                                                          "don't understand why staff insist on soap and water rather "
                                                          'than alcohol hand sanitizer.',
                                           'tasks': [   'Complain to the infection control nurse about feeling like an '
                                                        'outcast in an isolation side room.',
                                                        'Ask why hospital staff wear yellow gowns and gloves every '
                                                        'time they enter your room.',
                                                        "Ask why alcohol hand rub doesn't kill C. diff spores and why "
                                                        'soap and water is required.',
                                                        'Ask whether the hospital gave you this infection because your '
                                                        'bed area was contaminated.',
                                                        'Ask how many consecutive days of normal bowel movements are '
                                                        'required before isolation ends.',
                                                        'Agree to wash your hands with warm running water and soap '
                                                        'every time you use the commode.']},
                       'setting': 'Infectious Disease Isolation Ward',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'MEDIUM',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Clostridioides difficile: Hand Hygiene with Soap & Water and Contact Isolation'},
    {   'content': {   'candidate_card': {   'description': 'You are a surgical ward nurse assessing a 44-year-old '
                                                            'woman on Day 1 post-total thyroidectomy for multinodular '
                                                            'goiter. During morning vital signs, the patient casually '
                                                            "reports feeling 'weird prickling and tingling' around her "
                                                            'lips and fingertips.',
                                             'role': 'Nurse',
                                             'tasks': [   'Immediately recognize perioral and digital paresthesia as '
                                                          'classic early signs of acute post-surgical hypocalcemia '
                                                          '(parathyroid gland stunning).',
                                                          "Elicit and explain clinical tests gently (Chvostek's sign: "
                                                          "tapping facial nerve; Trousseau's sign: carpal spasm with "
                                                          'BP cuff).',
                                                          'Explain the physiological cause (parathyroid glands located '
                                                          'behind the thyroid can experience temporary vascular shock, '
                                                          'causing blood calcium to drop).',
                                                          'Reassure the patient while acting promptly: explain the '
                                                          'urgent need for a stat serum calcium blood draw and oral/IV '
                                                          'calcium replacement.',
                                                          'Assess vocal cord function (listening for hoarseness or '
                                                          'stridor from recurrent laryngeal nerve irritation).',
                                                          "Confirm the doctor's immediate review and maintain clear "
                                                          'communication to prevent panic.']},
                       'patient_card': {   'description': 'You are a 44-year-old woman on Day 1 after a total '
                                                          'thyroidectomy. You have developed a bizarre tingling and '
                                                          'prickling sensation around your lips and fingertips. You '
                                                          'wonder if it is just a harmless lingering effect of the '
                                                          'anesthetic.',
                                           'tasks': [   'Mention the strange pins-and-needles sensation around your '
                                                        'mouth and fingertips to the nurse.',
                                                        'Describe how the tingling started an hour ago and is '
                                                        'gradually spreading down your hands.',
                                                        'Ask whether this numbness is an allergic reaction, a stroke, '
                                                        'or lingering anesthesia.',
                                                        "Allow the nurse to test for facial twitching (Chvostek's "
                                                        "sign) and arm spasms (Trousseau's sign).",
                                                        'Ask why surgical trauma can stun the parathyroid glands and '
                                                        'cause blood calcium to drop.',
                                                        'Cooperate with urgent blood testing and accept intravenous or '
                                                        'oral calcium replacement therapy.']},
                       'setting': 'ENT / Endocrine Surgical Inpatient Ward',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'HARD',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Post-Thyroidectomy: Hypocalcemia Signs (Chvostek / Trousseau) and Voice Care'},
    {   'content': {   'candidate_card': {   'description': 'You are a pre-operative assessment nurse consulting with '
                                                            'a 52-year-old heavy smoker scheduled for elective total '
                                                            'hip replacement in 4 weeks. The orthopedic surgeon '
                                                            'informed the patient that surgery will be delayed unless '
                                                            'they quit smoking to lower surgical site infection and '
                                                            'non-union risks.',
                                             'role': 'Nurse',
                                             'tasks': [   "Acknowledge the patient's anxiety and defensiveness "
                                                          "regarding the surgeon's smoking ultimatum.",
                                                          'Explain the physiological impact of smoking on surgical '
                                                          'outcomes (carbon monoxide impairs oxygen delivery; nicotine '
                                                          'causes vasoconstriction, doubling wound infection and '
                                                          'implant loosening rates).',
                                                          'Highlight the immediate physiological benefits of quitting '
                                                          '4 weeks prior to surgery (carbon monoxide levels normalize '
                                                          'within 24 hours; airway ciliary clearance improves).',
                                                          'Explain Nicotine Replacement Therapy (NRT) options '
                                                          '(combination therapy: 24-hour transdermal patch for steady '
                                                          'background release plus fast-acting gum or inhalator for '
                                                          'breakthrough cravings).',
                                                          "Provide behavioral craving management tips (the 4 D's: "
                                                          'Delay, Deep breathe, Drink water, Distract).',
                                                          'Refer to the hospital/community Stop Smoking service and '
                                                          'arrange a telephone check-in.']},
                       'patient_card': {   'description': 'You are a 52-year-old heavy goods mechanic scheduled for '
                                                          'hip replacement in 4 weeks. The surgeon warned that your '
                                                          'operation will be cancelled unless you quit your 20-a-day '
                                                          'cigarette habit. You are stressed and feel you cannot quit '
                                                          'cold turkey.',
                                           'tasks': [   "Complain to the pre-op nurse that the surgeon's smoking "
                                                        'ultimatum is unfair and impossible.',
                                                        'Explain that you have smoked a pack a day for 32 years and '
                                                        'smoking is your main stress reliever.',
                                                        'Ask why smoking matters so much if the surgeon is operating '
                                                        'on your hip and not your lungs.',
                                                        'Ask how carbon monoxide and nicotine double the risk of wound '
                                                        'infection and joint loosening.',
                                                        'Ask how combination nicotine replacement therapy (patches '
                                                        'plus gum or inhalator) works.',
                                                        'Accept a referral to the hospital stop-smoking service and '
                                                        'set a quit date 4 weeks before surgery.']},
                       'setting': 'Pre-Admission / Pre-Operative Testing Clinic',
                       'timings': {'preparation_time': 180, 'speaking_time': 300}},
        'difficulty': 'MEDIUM',
        'duration': 480,
        'is_active': True,
        'question_type': 'ROLE_PLAY',
        'title': 'Pre-Operative Smoking Cessation and Nicotine Replacement Therapy'}]

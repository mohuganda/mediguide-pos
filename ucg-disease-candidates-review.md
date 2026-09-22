# Candidate disease and condition taxonomy — for review

Source: the 24 chapter files at `guidelines-platform/src/content/chapters_split/NN/index.md`
(Uganda Clinical Guidelines). Extracted, not authored: every name is the guideline's
own heading and every ICD-10 code is copied from the guideline text. Where the source
states no code, the cell is empty rather than guessed. Nothing has been seeded or committed.

Proposed mapping onto the existing schema:

| UCG level | Example | Proposed platform record |
|---|---|---|
| Chapter (24) | `Infectious Diseases` | `guideline_categories` row |
| Section (75) | `2.5 PROTOZOAL PARASITES` | not seeded (grouping only) |
| Numbered condition (351) | `2.5.2 Malaria` | `diseases` row, `parent_id` NULL |
| Sub-condition (119) | `2.5.2.2 Complicated/Severe Malaria` | `diseases` row, `parent_id` = its parent |

Totals: **470 candidates** — 351 parents, 119 children, 265 with an ICD-10 code, 85 needing a decision.

Review actions: strike anything that is not a clinical subject, merge the
duplicates, and confirm the two unparsed codes. Legend: `**!**` = needs a decision.

## 1. Emergencies and Trauma

| # | Name | Short | Aliases | ICD-10 | Flag |
|---|---|---|---|---|---|
| 1.1.1 | Anaphylactic Shock |  |  | T78.2 |  |
| 1.1.2 | Hypovolaemic Shock |  |  | R57.1 |  |
| 1.1.2.1 | &nbsp;&nbsp;↳ Hypovolaemic Shock in Children |  |  |  |  |
| 1.1.3 | Dehydration |  |  |  |  |
| 1.1.3.1 | &nbsp;&nbsp;↳ Dehydration in Children under 5 years |  |  |  |  |
| 1.1.3.2 | &nbsp;&nbsp;↳ Dehydration in Older Children and Adults |  |  |  |  |
| 1.1.4 | Fluids and Electrolytes Imbalances |  |  | E87.8 |  |
| 1.1.4.1 | &nbsp;&nbsp;↳ IV Fluid Management in Children |  |  | E87.8 |  |
| 1.1.5 | Febrile Convulsions |  |  | R56 |  |
| 1.1.6 | Hypoglycaemia |  |  | E16.2 |  |
| 1.2.1 | Bites and Stings |  |  |  |  |
| 1.2.1.1 | &nbsp;&nbsp;↳ Snakebites |  |  |  |  |
| 1.2.1.2 | &nbsp;&nbsp;↳ Insect Bites and Stings |  |  | T63.4 |  |
| 1.2.1.3 | &nbsp;&nbsp;↳ Animal and Human Bites |  |  | W50.3 W54.0 |  |
| 1.2.1.4 | &nbsp;&nbsp;↳ **!** Rabies Post Exposure Prophylaxis |  |  | Z20.3 Z23 | non-clinical-subject? |
| 1.2.1.5 | &nbsp;&nbsp;↳ **!** Rabies Vaccine Schedules |  |  |  | non-clinical-subject? |
| 1.2.2 | Fractures |  |  | S00-T88 |  |
| 1.2.3 | Burns |  |  | T20-T25 |  |
| 1.2.4 | Wounds |  |  | S00-T88 |  |
| 1.2.5 | Head Injuries |  |  | S00-S09 |  |
| 1.2.5.1 | &nbsp;&nbsp;↳ Traumatic Spinal Injury |  |  |  |  |
| 1.2.6 | Sexual Assault/Rape |  |  | Z04.4 |  |
| 1.3.1 | **!** General Management of Poisoning |  |  | T36-T50 | non-clinical-subject? |
| 1.3.1.2 | &nbsp;&nbsp;↳ Removal and Elimination of Ingested Poison |  |  |  |  |
| 1.3.2 | Acute Organophosphate Poisoning |  |  | T60.0 |  |
| 1.3.3 | Paraffin and Other Petroleum Products Poisoning |  |  | T53.7 |  |
| 1.3.4 | Acetylsalicylic Acid Poisoning |  | Aspirin | T39.0 |  |
| 1.3.5 | Paracetamol Poisoning |  |  | T39.1 |  |
| 1.3.6 | Iron Poisoning |  |  | T45.4 |  |
| 1.3.7 | Carbon Monoxide Poisoning |  |  |  |  |
| 1.3.8 | Barbiturate Poisoning |  |  | T42.3 |  |
| 1.3.9 | Opioid Poisoning |  |  | T40 |  |
| 1.3.10 | Warfarin Poisoning |  |  | T45.5 |  |
| 1.3.11 | Methyl Alcohol Poisoning |  | Methanol | T51.1 |  |
| 1.3.12 | Alcohol Poisoning |  | Ethanol | T51 |  |
| 1.3.12.1 | &nbsp;&nbsp;↳ Acute Alcohol Poisoning |  |  |  |  |
| 1.3.12.2 | &nbsp;&nbsp;↳ Chronic Alcohol Poisoning |  |  |  |  |
| 1.3.13 | Food Poisoning |  |  | A05 |  |

## 2. Infectious Diseases

| # | Name | Short | Aliases | ICD-10 | Flag |
|---|---|---|---|---|---|
| 2.1.1 | Anthrax |  |  |  |  |
| 2.1.2 | Brucellosis |  |  |  |  |
| 2.1.3 | Diphtheria |  |  | A36.9 |  |
| 2.1.4 | Leprosy/Hansen’s Disease |  |  | A30.0 |  |
| 2.1.5 | Meningitis |  |  | A39.0 G00 G01 G02 |  |
| 2.1.5.1 | &nbsp;&nbsp;↳ Neonatal Meningitis |  |  |  |  |
| 2.1.5.2 | &nbsp;&nbsp;↳ **!** Cryptococcal Meningitis |  |  | B45.1 | duplicate-name:2.1.5.2,3.1.10.2 |
| 2.1.5.3 | &nbsp;&nbsp;↳ TB Meningitis |  |  | A17.0 |  |
| 2.1.6 | Plague |  |  |  |  |
| 2.1.7 | Septicaemia |  |  |  |  |
| 2.1.7.1 | &nbsp;&nbsp;↳ Neonatal Septicaemia |  |  |  |  |
| 2.1.7.2 | &nbsp;&nbsp;↳ Septic Shock Management in Adults |  |  |  |  |
| 2.1.8 | Tetanus |  |  | A35 |  |
| 2.1.8.1 | &nbsp;&nbsp;↳ Neonatal Tetanus |  |  |  |  |
| 2.1.9 | Typhoid Fever |  | Enteric Fever | A01.00 |  |
| 2.1.10 | Typhus Fever |  |  | A75.9 |  |
| 2.2.1 | Candidiasis |  |  | B37 |  |
| 2.3.1 | Avian Influenza |  |  | J09.X2 |  |
| 2.3.2 | Chicken Pox |  |  | B01 |  |
| 2.3.3 | Measles |  |  | B05 |  |
| 2.3.4 | Poliomyelitis |  |  | A80.3 |  |
| 2.3.5 | Rabies |  |  | A82 |  |
| 2.3.6 | Viral Haemorrhagic Fevers |  |  |  |  |
| 2.3.6.1 | &nbsp;&nbsp;↳ Ebola and Marburg |  |  | A99 |  |
| 2.3.6.2 | &nbsp;&nbsp;↳ Yellow Fever |  |  |  |  |
| 2.3.7 | COVID-19 Disease |  |  |  |  |
| 2.4.1 | Intestinal Worms |  |  | B83.9 |  |
| 2.4.1.1 | &nbsp;&nbsp;↳ Taeniasis |  | Tapeworm | B68 |  |
| 2.4.2 | Echinococcosis |  | Hydatid Disease | B67 |  |
| 2.4.3 | Dracunculiasis |  | Guinea Worm | B72 |  |
| 2.4.4 | Lymphatic Filariasis |  |  | B74.9 |  |
| 2.4.5 | Onchocerciasis |  | River Blindness | B73.0 |  |
| 2.4.6 | Schistosomiasis |  | Bilharziasis | B65.1 |  |
| 2.5.1 | Leishmaniasis |  |  | B55 |  |
| 2.5.2 | Malaria |  |  | B50 |  |
| 2.5.2.1 | &nbsp;&nbsp;↳ Uncomplicated Malaria |  |  |  |  |
| 2.5.2.2 | &nbsp;&nbsp;↳ Complicated/Severe Malaria |  |  | B50.0 B50.8 |  |
| 2.5.2.3 | &nbsp;&nbsp;↳ **!** Management of Complications of Severe Malaria |  |  |  | non-clinical-subject? |
| 2.5.2.4 | &nbsp;&nbsp;↳ **!** Malaria Prophylaxis |  |  |  | non-clinical-subject? |
| 2.5.2.5 | &nbsp;&nbsp;↳ Malaria Prevention and Control |  |  |  |  |

## 3. HIV/AIDS and Sexually Transmitted Infections

| # | Name | Short | Aliases | ICD-10 | Flag |
|---|---|---|---|---|---|
| 3.1.1 | Clinical Features of HIV |  |  |  |  |
| 3.1.2 | Diagnosis and Investigations of HIV |  |  |  |  |
| 3.1.4 | **!** General Principles of Antiretroviral Treatment | ART |  |  | non-clinical-subject? |
| 3.1.5 | **!** Recommended First-Line Regimens in Adults, Adolescents, Pregnant Women and Children |  |  |  | non-clinical-subject? |
| 3.1.6 | **!** Monitoring of ART |  |  |  | non-clinical-subject? |
| 3.1.7 | ARV Toxicity |  |  |  |  |
| 3.1.8 | **!** Recommended Second-Line Regimens in Adults, Adolescents, Pregnant Women and Children |  |  |  | non-clinical-subject? |
| 3.1.9 | Mother-to-Child Transmission of HIV |  |  |  |  |
| 3.1.9.1 | &nbsp;&nbsp;↳ **!** Management of HIV-Positive Pregnant Mother |  |  |  | non-clinical-subject? |
| 3.1.9.2 | &nbsp;&nbsp;↳ HIV-Exposed Infant Care Services |  |  |  |  |
| 3.1.9.3 | &nbsp;&nbsp;↳ **!** Care of HIV-Exposed Infant |  |  |  | non-clinical-subject? |
| 3.1.10 | Opportunistic Infections in HIV |  |  |  |  |
| 3.1.10.1 | &nbsp;&nbsp;↳ Tuberculosis and HIV Co-Infection |  |  |  |  |
| 3.1.10.2 | &nbsp;&nbsp;↳ **!** Cryptococcal Meningitis |  |  | B45 | duplicate-name:2.1.5.2,3.1.10.2 |
| 3.1.10.3 | &nbsp;&nbsp;↳ Hepatitis B and HIV Co-Infection |  |  | B18 |  |
| 3.1.10.4 | &nbsp;&nbsp;↳ Pneumocystis Pneumonia |  |  | B59 |  |
| 3.1.10.5 | &nbsp;&nbsp;↳ Other Diseases |  |  |  |  |
| 3.1.11 | **!** Prevention of HIV |  |  |  | non-clinical-subject? |
| 3.1.11.1 | &nbsp;&nbsp;↳ **!** Post-Exposure Prophylaxis |  |  | Z20.6 | non-clinical-subject? |
| 3.1.11.2 | &nbsp;&nbsp;↳ **!** Pre-Exposure Prophylaxis |  | PrEP |  | non-clinical-subject? |
| 3.1.12 | Psychosocial Support for HIV-Positive Persons |  |  |  |  |
| 3.2.1 | Urethral Discharge Syndrome |  | Male | R36 |  |
| 3.2.2 | Abnormal Vaginal Discharge Syndrome |  |  | N76 |  |
| 3.2.3 | **!** Pelvic Inflammatory Disease | PID |  |  | duplicate-name:3.2.3,14.1.2 |
| 3.2.4 | Genital Ulcer Disease Syndrome | GUD |  | N76.5 N48.5 |  |
| 3.2.5 | Inguinal Swelling |  | Bubo |  |  |
| 3.2.6 | Genital Warts |  |  | A63.0 |  |
| 3.2.7 | Syphilis |  |  | A51 |  |
| 3.2.8 | Other STI Syndromes |  |  |  |  |
| 3.2.8.1 | &nbsp;&nbsp;↳ Balanitis |  |  | N48.1 |  |
| 3.2.8.2 | &nbsp;&nbsp;↳ Painful Scrotal Swelling |  |  | N45 |  |
| 3.2.9 | Congenital STI Syndromes |  |  |  |  |
| 3.2.9.1 | &nbsp;&nbsp;↳ Neonatal Conjunctivitis |  | Ophthalmia Neonatorum | P39.1 |  |
| 3.2.9.2 | &nbsp;&nbsp;↳ Congenital Syphilis |  |  | A50 |  |

## 4. Cardiovascular Diseases

| # | Name | Short | Aliases | ICD-10 | Flag |
|---|---|---|---|---|---|
| 4.1.1 | Deep Vein Thrombosis / Pulmonary Embolism | DVT/PE |  | I82.409 |  |
| 4.1.2 | Infective Endocarditis |  |  | I33.0 |  |
| 4.1.3 | Heart Failure |  |  | I50 |  |
| 4.1.4 | Pulmonary Oedema |  |  | I50.21 |  |
| 4.1.5 | Atrial Fibrillation |  |  | I48 |  |
| 4.1.6 | Hypertension |  |  | I10 |  |
| 4.1.6.1 | &nbsp;&nbsp;↳ Hypertensive Emergencies and Urgency |  |  | I16.2 |  |
| 4.1.7 | Ischaemic Heart Disease |  | Coronary Heart Disease | I20 I21 I25 |  |
| 4.1.8 | Pericarditis |  |  | I30 |  |
| 4.1.9 | Rheumatic Fever |  |  | I00 I01 |  |
| 4.1.10 | Rheumatic Heart Disease |  |  | I05-I09 |  |
| 4.1.11 | Stroke |  |  | I63 |  |

## 5. Respiratory Diseases

| # | Name | Short | Aliases | ICD-10 | Flag |
|---|---|---|---|---|---|
| 5.1.1 | Asthma |  |  |  |  |
| 5.1.1.1 | &nbsp;&nbsp;↳ Acute Asthma |  |  |  |  |
| 5.1.1.2 | &nbsp;&nbsp;↳ Chronic Asthma |  |  |  |  |
| 5.2.1 | Bronchiolitis |  |  | J21 |  |
| 5.2.2 | Acute Bronchitis |  |  | J20 |  |
| 5.2.3 | Coryza |  | Common Cold | J00 |  |
| 5.2.4 | Acute Epiglottitis |  |  | J05.1 |  |
| 5.2.5 | Influenza |  | Flu | J09-J11 |  |
| 5.2.6 | Laryngitis |  |  | J04 |  |
| 5.2.7 | Acute Laryngotracheobronchitis |  | Croup | J05.0 |  |
| 5.2.8 | Pertussis |  | Whooping Cough | A37 |  |
| 5.2.9 | Pneumonia |  |  | J13-J18 |  |
| 5.2.9.1 | &nbsp;&nbsp;↳ Pneumonia in an Infant |  | Up to 2 Months |  |  |
| 5.2.9.2 | &nbsp;&nbsp;↳ Pneumonia in a Child of 2 months to 5 years |  |  |  |  |
| 5.2.9.3 | &nbsp;&nbsp;↳ Pneumonia in Children above 5 years and Adults |  |  |  |  |
| 5.2.9.4 | &nbsp;&nbsp;↳ Pneumonia by Specific Organisms |  |  |  |  |
| 5.2.9.5 | &nbsp;&nbsp;↳ Pneumocystis jirovecii Pneumonia |  |  |  |  |
| 5.2.9.6 | &nbsp;&nbsp;↳ Lung Abscess |  |  | J85.0-J85.1 |  |
| 5.3.1 | **!** Definition, Clinical Features and Diagnosis of TB |  |  |  | non-clinical-subject? |
| 5.3.1.1 | &nbsp;&nbsp;↳ Tuberculosis in Children and Adolescents |  |  |  |  |
| 5.3.1.2 | &nbsp;&nbsp;↳ Drug-Resistant TB |  |  |  |  |
| 5.3.1.3 | &nbsp;&nbsp;↳ Post-TB Patient Management |  |  |  |  |
| 5.3.2 | **!** Management of TB |  |  |  | non-clinical-subject? |
| 5.3.2.1 | &nbsp;&nbsp;↳ Anti-TB Drug Side Effects |  |  |  |  |
| 5.3.2.2 | &nbsp;&nbsp;↳ Prevention and Infection Control of TB |  |  |  |  |
| 5.3.2.3 | &nbsp;&nbsp;↳ Tuberculosis Preventive Treatment |  |  |  |  |
| 5.3.2.5 | &nbsp;&nbsp;↳ TB Preventive Treatment Dosing Chart |  |  |  |  |

## 6. Gastrointestinal and Hepatic Diseases

| # | Name | Short | Aliases | ICD-10 | Flag |
|---|---|---|---|---|---|
| 6.1.1 | Acute Appendicitis |  |  | K35-K37 |  |
| 6.1.2 | Acute Pancreatitis |  |  | K85 |  |
| 6.1.3 | Upper Gastrointestinal Bleeding |  |  |  |  |
| 6.1.4 | Peritonitis |  |  |  |  |
| 6.1.5 | **!** Diarrhoea |  |  |  | code-text-unparsed |
| 6.2.1 | Amoebiasis |  |  | A06 |  |
| 6.2.2 | Bacillary Dysentery |  | Shigellosis | A03.9 |  |
| 6.2.3 | Cholera |  |  | A00 |  |
| 6.2.4 | Giardiasis |  |  | A07.1 |  |
| 6.3.1 | Dysphagia |  |  | R13.1 |  |
| 6.3.2 | Dyspepsia |  |  | K30 |  |
| 6.3.4 | Gastritis |  |  | K27 |  |
| 6.3.5 | Peptic Ulcer Disease | PUD |  |  |  |
| 6.3.6 | Chronic Pancreatitis |  |  | K86.0-K86.1 |  |
| 6.4.1 | Constipation |  |  | K59.0 |  |
| 6.4.2 | Haemorrhoids and Anal Fissures |  | Piles | K64 K60.0 K60.2 |  |
| 6.5.1 | Viral Hepatitis |  |  |  |  |
| 6.5.1.1 | &nbsp;&nbsp;↳ Acute Hepatitis |  |  | B15 B16 B17 B19 |  |
| 6.5.1.2 | &nbsp;&nbsp;↳ Chronic Hepatitis |  |  | B18 |  |
| 6.5.2 | Hepatitis B Special Situations |  |  |  |  |
| 6.5.2.1 | &nbsp;&nbsp;↳ Inactive Hepatitis B Carriers |  |  | B18.1 |  |
| 6.5.2.2 | &nbsp;&nbsp;↳ Pregnant Mother HBsAg Positive |  |  | B18.1 |  |
| 6.5.3 | Chronic Hepatitis C Infection |  |  | B18.2 |  |
| 6.5.4 | Liver Cirrhosis |  |  | K74 K70.3 |  |
| 6.5.4.1 | &nbsp;&nbsp;↳ Ascites |  |  | R18 K70.31 K70.11 K71.51 |  |
| 6.5.4.2 | &nbsp;&nbsp;↳ Spontaneous Bacterial Peritonitis | SBP |  | K65.2 |  |
| 6.5.4.3 | &nbsp;&nbsp;↳ Hepatic Encephalopathy | HE |  | K70.41 K71.11 K72.11 K72.91 |  |
| 6.5.4.4 | &nbsp;&nbsp;↳ Hepatocellular Carcinoma |  |  | C22.0 |  |
| 6.5.5 | Hepatic Schistosomiasis |  |  | B65.1 |  |
| 6.5.6 | Drug-Induced Liver Injury |  |  | K71 |  |
| 6.5.7 | Jaundice |  | Hyperbilirubinaemia | R17 |  |
| 6.5.8 | Gallstones / Biliary Colic |  |  | K80 |  |
| 6.5.9 | Acute Cholecystitis / Cholangitis |  |  | K81 |  |

## 7. Renal and Urinary Diseases

| # | Name | Short | Aliases | ICD-10 | Flag |
|---|---|---|---|---|---|
| 7.1.1 | Acute Renal Failure |  |  | N17 |  |
| 7.1.2 | Chronic Kidney Disease | CKD |  | N18 |  |
| 7.1.3 | **!** Use of Medicines in Renal Failure |  |  |  | non-clinical-subject? |
| 7.1.4 | Glomerulonephritis |  |  | N00-N01 |  |
| 7.1.5 | Nephrotic Syndrome |  |  | N04 |  |
| 7.2.1 | Acute Cystitis |  |  | N30 |  |
| 7.2.2 | Acute Pyelonephritis |  |  | N10 |  |
| 7.2.3 | Prostatitis |  |  | N41 |  |
| 7.2.4 | Renal Colic |  |  | N23 |  |
| 7.2.5 | Benign Prostatic Hyperplasia |  |  | N40 |  |
| 7.2.6 | Bladder Outlet Obstruction |  |  |  |  |
| 7.2.7 | Urinary Incontinence |  |  | N39.3-N39.4 |  |

## 8. Endocrine and Metabolic Diseases

| # | Name | Short | Aliases | ICD-10 | Flag |
|---|---|---|---|---|---|
| 8.1.1 | Addison’s Disease |  |  | E27.1-E27.4 |  |
| 8.1.2 | Cushing’s Syndrome |  |  | E24 |  |
| 8.1.3 | Diabetes Mellitus |  |  | E08-E13 |  |
| 8.1.4 | Diabetic Ketoacidosis and Hyperosmolar Hyperglycaemic State | DKA | HHS | E10.1 E11.0 |  |
| 8.1.5 | Goitre |  |  | E04 |  |
| 8.1.6 | Hyperthyroidism |  |  | E05 |  |
| 8.1.7 | Hypothyroidism |  |  | E03 |  |
| 8.1.8 | Central Precocious Puberty |  |  |  |  |

## 9. Mental, Neurological and Substance Use Disorders

| # | Name | Short | Aliases | ICD-10 | Flag |
|---|---|---|---|---|---|
| 9.1.1 | Epilepsy |  |  | G40 |  |
| 9.1.2 | Nodding Disease |  |  | G40.4 |  |
| 9.1.3 | Headache |  |  | R51 |  |
| 9.1.3.1 | &nbsp;&nbsp;↳ Migraine |  |  | G43 |  |
| 9.1.4 | Dementia |  |  | F01 F03 |  |
| 9.1.5 | Parkinsonism |  |  | G20 G21 |  |
| 9.1.6 | Delirium |  |  | F05 |  |
| 9.2.1 | Anxiety |  |  | F40-F48 |  |
| 9.2.2 | Depression |  |  |  |  |
| 9.2.2.1 | &nbsp;&nbsp;↳ Postnatal Depression |  |  |  |  |
| 9.2.2.2 | &nbsp;&nbsp;↳ Suicidal Behaviour / Self Harm |  |  | T14.91 Z91.5 |  |
| 9.2.3 | Bipolar Disorder |  | Mania | F30 F31 |  |
| 9.2.4 | Psychosis |  |  | F20-F29 |  |
| 9.2.4.1 | &nbsp;&nbsp;↳ Postnatal Psychosis |  |  | F53 |  |
| 9.2.5 | Alcohol Use Disorders |  |  | F10 |  |

## 10. Musculoskeletal and Joint Diseases

| # | Name | Short | Aliases | ICD-10 | Flag |
|---|---|---|---|---|---|
| 10.1.1 | Pyogenic Arthritis |  | Septic Arthritis | M00 |  |
| 10.1.2 | Osteomyelitis |  |  | M86 |  |
| 10.1.3 | Pyomyositis |  |  | M60.0 |  |
| 10.1.4 | Tuberculosis of the Spine |  | Pott's Disease | A18.01 |  |
| 10.2.1 | Rheumatoid Arthritis |  |  | M05 |  |
| 10.2.2 | Gout Arthritis |  |  | M10 |  |
| 10.2.3 | Osteoarthritis |  |  | M15-M19 |  |

## 11. Blood Diseases and Blood Transfusion Guidelines

| # | Name | Short | Aliases | ICD-10 | Flag |
|---|---|---|---|---|---|
| 11.1.1 | Anaemia |  |  |  |  |
| 11.1.1.1 | &nbsp;&nbsp;↳ Iron Deficiency Anaemia |  |  | D50 |  |
| 11.1.1.2 | &nbsp;&nbsp;↳ Megaloblastic Anaemia |  |  | D51-D52 |  |
| 11.1.1.3 | &nbsp;&nbsp;↳ Normocytic Anaemia |  |  |  |  |
| 11.1.2 | Bleeding Disorders |  |  |  |  |
| 11.1.3 | Sickle Cell Disease |  |  | D57 |  |
| 11.2.1 | **!** General Principles of Good Clinical Practice in Transfusion Medicine |  |  |  | non-clinical-subject? |
| 11.2.2 | Blood and Blood Products: Characteristics and Indications |  |  |  |  |
| 11.2.2.1 | &nbsp;&nbsp;↳ Whole Blood |  |  |  |  |
| 11.2.2.2 | &nbsp;&nbsp;↳ Red Cell Concentrates / Packed Red Cells |  |  |  |  |
| 11.2.2.3 | &nbsp;&nbsp;↳ **!** Clinical Indications for Blood Transfusion |  |  |  | non-clinical-subject? |
| 11.2.3 | **!** Adverse Reactions Following Transfusion |  |  |  | non-clinical-subject? |
| 11.2.3.1 | &nbsp;&nbsp;↳ **!** Acute Transfusion Reactions |  |  |  | non-clinical-subject? |

## 12. Oncology

| # | Name | Short | Aliases | ICD-10 | Flag |
|---|---|---|---|---|---|
| 12.1.1 | Special Groups at Increased Risk of Cancer |  |  |  |  |
| 12.1.2 | Early Signs and Symptoms |  |  |  |  |
| 12.1.2.1 | &nbsp;&nbsp;↳ Urgent Signs and Symptoms |  |  |  |  |
| 12.2.1 | Primary Prevention |  |  |  |  |
| 12.2.1.1 | &nbsp;&nbsp;↳ Control of Risk Factors |  |  |  |  |
| 12.2.2 | Secondary Prevention |  |  |  |  |
| 12.3.1 | Common Cancers in Children |  |  |  |  |
| 12.3.2 | Common Cancers in Adults |  |  |  |  |

## 13. Palliative Care

| # | Name | Short | Aliases | ICD-10 | Flag |
|---|---|---|---|---|---|
| 13.1.1 | Clinical Features and Investigations |  |  |  |  |
| 13.1.2 | Nociceptive Pain Management |  |  |  |  |
| 13.1.2.1 | &nbsp;&nbsp;↳ Pain Management in Adults |  |  |  |  |
| 13.1.2.3 | &nbsp;&nbsp;↳ Pain Management in Children |  |  |  |  |
| 13.1.3 | Neuropathic Pain |  |  |  |  |
| 13.1.4 | Back or Bone Pain |  |  |  |  |
| 13.2.1 | Breathlessness |  |  | R06 |  |
| 13.2.2 | Nausea and Vomiting |  |  | R11 |  |
| 13.2.3 | Pressure Ulcer / Decubitus Ulcers |  |  | L89 |  |
| 13.2.4 | Fungating Wounds |  |  |  |  |
| 13.2.5 | Anorexia and Cachexia |  |  | R63.0 R64 |  |
| 13.2.6 | Hiccup |  |  |  |  |
| 13.2.7 | Dry or Painful Mouth |  |  | R68.2 |  |
| 13.2.8 | Other Symptoms |  |  |  |  |
| 13.2.9 | End of Life Care |  |  |  |  |

## 14. Gynaecological Conditions

| # | Name | Short | Aliases | ICD-10 | Flag |
|---|---|---|---|---|---|
| 14.1.1 | Dysmenorrhoea |  |  | N94.6 |  |
| 14.1.2 | **!** Pelvic Inflammatory Disease | PID |  | N70-N73 | duplicate-name:3.2.3,14.1.2 |
| 14.1.3 | Abnormal Uterine Bleeding |  |  | N39.9 |  |
| 14.1.4 | Menopause |  |  | Z78.0 |  |

## 15. Family Planning (FP)

| # | Name | Short | Aliases | ICD-10 | Flag |
|---|---|---|---|---|---|
| 15.1.1 | **!** Provide Information about FP including Pre-Conception Care to Different Groups |  |  |  | non-clinical-subject? |
| 15.1.2 | Counsel High-Risk Clients |  |  |  |  |
| 15.1.3 | Pre-Conception Care with Clients Who Desire to Conceive |  |  |  |  |
| 15.1.4 | Discuss with People Living with HIV: Special Considerations for HIV Transmission |  |  |  |  |
| 15.1.5 | **!** Educate and Counsel Clients to Make an Informed Choice of FP Method |  |  |  | non-clinical-subject? |
| 15.1.6 | Obtain and Record Client History |  |  |  |  |
| 15.1.7 | Perform a Physical Assessment |  |  |  |  |
| 15.1.8 | Perform a Pelvic Examination |  |  |  |  |
| 15.1.9 | **!** Manage Client for Chosen FP Method |  |  |  | non-clinical-subject? |
| 15.1.10 | Summary of Medical Eligibility for Contraceptives |  |  |  |  |
| 15.2.1 | **!** Condom |  | Male | Z30.0 Z30.49 | duplicate-name:15.2.1,15.2.2 |
| 15.2.2 | **!** Condom |  | Female | Z30.0 Z30.49 | duplicate-name:15.2.1,15.2.2 |
| 15.2.3 | Combined Oral Contraceptive Pill | COC |  | Z30.0 Z30.41 |  |
| 15.2.4 | Progestogen-Only Pill | POP |  | Z30.0 Z30.41 |  |
| 15.2.5 | Injectable Progestogen-Only Contraceptive |  |  | Z30.0 Z30.42 |  |
| 15.2.6 | Progestogen-Only Sub-Dermal Implant |  |  | Z30.0 Z30.46 |  |
| 15.2.7 | Emergency Contraception |  | Pill and IUD | Z30.012 |  |
| 15.2.8 | Intrauterine Device | IUD |  | Z30.014 |  |
| 15.2.9 | **!** Natural FP: Cervical Mucus Method and Moon Beads | CMM |  | Z30.02 | non-clinical-subject? |
| 15.2.10 | **!** Natural FP: Lactational Amenorrhoea Method | LAM |  | Z30.02 | non-clinical-subject? |
| 15.2.11 | Surgical Contraception for Men: Vasectomy |  |  | Z30.2 |  |
| 15.2.12 | Surgical Contraception for Women: Tubal Ligation |  |  | Z30.2 |  |

## 16. Obstetric Conditions

| # | Name | Short | Aliases | ICD-10 | Flag |
|---|---|---|---|---|---|
| 16.1.1 | Goal-Oriented Antenatal Care Protocol |  |  |  |  |
| 16.1.2 | **!** Management of Common Complaints during Pregnancy |  |  |  | non-clinical-subject? |
| 16.1.3 | High Risk Pregnancy | HRP |  | O09 |  |
| 16.2.1 | Anaemia in Pregnancy |  |  | O99.019 |  |
| 16.2.2 | Pregnancy and HIV Infection |  |  |  |  |
| 16.2.2.1 | &nbsp;&nbsp;↳ Care for HIV-Positive Women |  | eMTCT | O98.719 |  |
| 16.2.2.2 | &nbsp;&nbsp;↳ **!** Counselling for HIV-Positive Mothers |  |  |  | non-clinical-subject? |
| 16.2.3 | Chronic Hypertension in Pregnancy |  |  | O10 O13 |  |
| 16.2.4 | Malaria in Pregnancy |  |  | B54 |  |
| 16.2.5 | Diabetes in Pregnancy |  |  | O24 |  |
| 16.3.1 | Hyperemesis Gravidarum |  |  | O21 |  |
| 16.3.2 | Vaginal Bleeding in Early Pregnancy / Abortion |  |  | O20 |  |
| 16.3.3 | Ectopic Pregnancy |  |  | O00 |  |
| 16.3.4 | Premature Rupture of Membranes |  | PROM and PPROM | O42 |  |
| 16.3.5 | Chorioamnionitis |  |  |  |  |
| 16.4.2 | Induction of Labour |  |  |  |  |
| 16.4.3 | Obstructed Labour |  |  | O64-O66 |  |
| 16.4.4 | Ruptured Uterus |  |  | O71.1 |  |
| 16.4.5 | Retained Placenta |  |  | O73 |  |
| 16.4.6 | Postpartum Haemorrhage | PPH |  | O72 |  |
| 16.4.8 | **!** Care of Mother and Baby Immediately After Delivery |  |  | Z39 | non-clinical-subject? |
| 16.4.8.1 | &nbsp;&nbsp;↳ **!** Care of Mother Immediately After Delivery |  |  |  | non-clinical-subject? |
| 16.4.8.2 | &nbsp;&nbsp;↳ **!** Care of Baby Immediately After Delivery |  |  |  | non-clinical-subject? |
| 16.5.1 | Newborn Resuscitation |  |  | P22 |  |
| 16.5.2 | **!** General Care of Newborn After Delivery |  |  |  | non-clinical-subject? |
| 16.5.1.2 | &nbsp;&nbsp;↳ Postpartum Examination of the Mother Up to 6 Weeks |  |  |  |  |
| 16.5.3 | **!** Extra Care of Small Babies or Twins in the First Days of Life |  |  |  | non-clinical-subject? |
| 16.5.4 | Newborn Hygiene at Home |  |  |  |  |
| 16.6.1 | Postpartum Care |  |  | Z39 |  |
| 16.6.1.1 | &nbsp;&nbsp;↳ **!** Postpartum Counselling |  |  |  | non-clinical-subject? |
| 16.6.3 | Mastitis / Breast Abscess |  |  | O91 |  |

## 17. Childhood Illness

| # | Name | Short | Aliases | ICD-10 | Flag |
|---|---|---|---|---|---|
| 17.1.1 | Newborn Examination / Danger Signs |  |  |  |  |
| 17.1.2 | **!** Assess for Special Treatment Needs, Local Infection, and Jaundice |  |  |  | non-clinical-subject? |
| 17.2.1 | **!** Check for Very Severe Disease and Local Bacterial Infection |  |  |  | non-clinical-subject? |
| 17.2.2 | **!** Check for Jaundice |  |  |  | non-clinical-subject? |
| 17.2.3 | **!** Check for Diarrhoea/Dehydration |  |  |  | non-clinical-subject? |
| 17.2.4 | **!** Check for HIV Infection |  |  |  | non-clinical-subject? |
| 17.2.5 | **!** Check for Feeding Problem or Low Weight-for-Age |  |  |  | non-clinical-subject? |
| 17.2.5.1 | &nbsp;&nbsp;↳ All Young Infants Except HIV-exposed Infants Not Breastfed |  |  |  |  |
| 17.2.5.2 | &nbsp;&nbsp;↳ **!** HIV-exposed Non Breastfeeding Infants |  |  |  | non-clinical-subject? |
| 17.2.6 | **!** Check Young Infant’s Immunization Status |  |  |  | non-clinical-subject? |
| 17.2.7 | **!** Assess Other Problems |  |  |  | non-clinical-subject? duplicate-name:17.2.7,17.3.9 |
| 17.2.8 | **!** Assess Mother’s Health Needs |  |  |  | non-clinical-subject? |
| 17.2.9 | Summary of IMNCI Medicines Used for Young Infants |  |  |  |  |
| 17.2.10 | **!** Counsel the Mother |  |  |  | duplicate-name:17.2.10,17.3.11 |
| 17.3.1 | **!** Check for General Danger Signs |  |  |  | non-clinical-subject? |
| 17.3.2 | **!** Check for Cough or Difficult Breathing |  |  |  | non-clinical-subject? |
| 17.3.3 | Child Has Diarrhoea |  |  |  |  |
| 17.3.4 | **!** Check for Fever |  |  |  | non-clinical-subject? |
| 17.3.5 | **!** Check for Ear Problem |  |  |  | non-clinical-subject? |
| 17.3.6 | **!** Check for Malnutrition and Feeding Problems |  |  |  | non-clinical-subject? |
| 17.3.7 | **!** Check for Anaemia |  |  |  | non-clinical-subject? |
| 17.3.8 | **!** Check Immunization, Vitamin A, Deworming |  |  |  | non-clinical-subject? |
| 17.3.9 | **!** Assess Other Problems |  |  |  | non-clinical-subject? duplicate-name:17.2.7,17.3.9 |
| 17.3.10 | Summary of Medicines Used |  |  |  |  |
| 17.3.10.1 | &nbsp;&nbsp;↳ Medicines Used Only in Health Centers |  |  |  |  |
| 17.3.10.2 | &nbsp;&nbsp;↳ Medicines for Home Use |  |  |  |  |
| 17.3.10.3 | &nbsp;&nbsp;↳ Treatment of Local Infections at Home |  |  |  |  |
| 17.3.11 | **!** Counsel the Mother |  |  |  | duplicate-name:17.2.10,17.3.11 |
| 17.3.12.1 | &nbsp;&nbsp;↳ **!** Feeding Recommendation during Illness |  |  |  | orphan-child non-clinical-subject? |
| 17.3.12.2 | &nbsp;&nbsp;↳ **!** Assessing Appetite and Feeding |  |  |  | orphan-child non-clinical-subject? |
| 17.3.12.3 | &nbsp;&nbsp;↳ **!** Feeding Recommendations |  |  |  | orphan-child non-clinical-subject? |
| 17.3.12.4 | &nbsp;&nbsp;↳ **!** Counselling for Feeding Problems |  |  |  | orphan-child non-clinical-subject? |
| 17.3.12.5 | &nbsp;&nbsp;↳ **!** Mother’s Health |  |  |  | orphan-child |

## 18. Immunization

| # | Name | Short | Aliases | ICD-10 | Flag |
|---|---|---|---|---|---|
| 18.1.1 | **!** National Immunization Schedule |  |  |  | non-clinical-subject? |
| 18.1.2 | **!** Hepatitis B Vaccination |  |  |  | non-clinical-subject? |
| 18.1.3 | **!** Yellow Fever Vaccination |  |  |  | non-clinical-subject? |
| 18.1.4 | Tetanus Prevention |  |  |  |  |
| 18.2.3.1 | &nbsp;&nbsp;↳ **!** Prophylaxis Against Neonatal Tetanus |  |  |  | orphan-child non-clinical-subject? |
| 18.2.4 | **!** Vaccination Against COVID-19 |  |  |  | non-clinical-subject? |

## 19. Nutrition

| # | Name | Short | Aliases | ICD-10 | Flag |
|---|---|---|---|---|---|
| 19.1.1 | **!** Infant and Young Child Feeding | IYCF |  |  | non-clinical-subject? |
| 19.1.2 | Nutrition in HIV/AIDS |  |  |  |  |
| 19.1.3 | Nutrition in Diabetes |  |  |  |  |
| 19.2.1 | **!** Introduction on Malnutrition |  |  |  | non-clinical-subject? |
| 19.2.1.1 | &nbsp;&nbsp;↳ **!** Classification of Malnutrition |  |  |  | non-clinical-subject? |
| 19.2.1.2 | &nbsp;&nbsp;↳ Assessing Malnutrition in Children 6 months to 5 years |  |  |  |  |
| 19.2.2 | **!** Management of Acute Malnutrition in Children |  |  |  | non-clinical-subject? |
| 19.2.2.1 | &nbsp;&nbsp;↳ **!** Management of Moderate Acute Malnutrition |  |  |  | non-clinical-subject? |
| 19.2.2.2 | &nbsp;&nbsp;↳ **!** Management of Uncomplicated Severe Acute Malnutrition |  |  |  | non-clinical-subject? |
| 19.2.2.3 | &nbsp;&nbsp;↳ **!** Management of Complicated Severe Acute Malnutrition |  |  |  | non-clinical-subject? |
| 19.2.2.4 | &nbsp;&nbsp;↳ Treatment of Associated Conditions |  |  |  |  |
| 19.2.2.5 | &nbsp;&nbsp;↳ Discharge from Nutritional Programme |  |  |  |  |
| 19.2.3 | SAM in Infants Less than 6 Months |  |  |  |  |
| 19.2.4 | Obesity and Overweight |  |  | E66 |  |

## 20. Eye Conditions

| # | Name | Short | Aliases | ICD-10 | Flag |
|---|---|---|---|---|---|
| 20.1.1 | **!** Notes on Use of Eye Preparations |  |  |  | non-clinical-subject? |
| 20.1.2 | Conjunctivitis |  | Red Eye | H10 |  |
| 20.1.3 | Stye |  | Hordeolum | H00 |  |
| 20.1.4 | Trachoma |  |  | A71 |  |
| 20.1.5 | Keratitis |  |  | H16 |  |
| 20.1.6 | Uveitis |  |  | H20 |  |
| 20.1.7 | Orbital Cellulitis |  |  | H05.01 |  |
| 20.1.8 | Postoperative Endophthalmitis |  |  | H44.0 |  |
| 20.1.9 | Xerophthalmia |  |  | E50 |  |
| 20.2.1 | Cataract |  |  | H27 |  |
| 20.2.1.1 | &nbsp;&nbsp;↳ Paediatric Cataract |  |  | H26.0 |  |
| 20.2.2 | Glaucoma |  |  | H40 |  |
| 20.2.3 | Diabetic Retinopathy |  |  | E10.31 E11.31 |  |
| 20.2.4 | Refractive Errors |  |  | H52 |  |
| 20.2.5 | Low Vision |  |  | H54 |  |
| 20.2.5.1 | &nbsp;&nbsp;↳ Vision Loss |  |  | H54 |  |
| 20.3.1 | Foreign Body in the Eye |  |  | T15 |  |
| 20.3.2 | Ocular and Adnexa Injuries |  |  |  |  |
| 20.3.2.1 | &nbsp;&nbsp;↳ Blunt Injuries |  |  | S05.1 |  |
| 20.3.2.2 | &nbsp;&nbsp;↳ Penetrating Eye Injuries |  |  | S05.2 |  |
| 20.3.2.3 | &nbsp;&nbsp;↳ Chemical Injuries to the Eye |  |  | S05.8 |  |
| 20.4.1 | Retinoblastoma |  |  | C69.2 |  |
| 20.4.2 | Squamous Cell Carcinoma of Conjunctiva |  |  | C69.0 |  |

## 21. Ear, Nose & Throat Conditions

| # | Name | Short | Aliases | ICD-10 | Flag |
|---|---|---|---|---|---|
| 21.1.1 | Foreign Body in the Ear |  |  | T16 |  |
| 21.1.2 | Wax in the Ear |  |  | H61.2 |  |
| 21.1.3 | Otitis External |  |  | H60 |  |
| 21.1.4 | Otitis Media |  | Suppurative | H66 |  |
| 21.1.5 | Glue Ear |  | Otitis Media with Effusion | H65 |  |
| 21.1.6 | Mastoiditis |  |  | H70.0 |  |
| 21.2.1 | Foreign Body in the Nose |  |  | T17.0 |  |
| 21.2.2 | Epistaxis |  | Nose Bleeding | R04.0 |  |
| 21.2.3 | Nasal Allergy |  |  | J30 |  |
| 21.2.4 | Acute Sinusitis |  |  | J01 |  |
| 21.2.5 | Atrophic Rhinitis |  |  |  |  |
| 21.2.6 | Adenoid Disease |  |  | J35.02 J35.2 |  |
| 21.3.1 | Foreign Body in the Airway | FB |  | T17 |  |
| 21.3.2 | Foreign Body in the Food Passage |  |  | T18 |  |
| 21.3.3 | Pharyngitis |  | Sore Throat | J02 |  |
| 21.3.4 | Pharyngo-Tonsillitis |  |  | J03 |  |
| 21.3.5 | Peritonsillar Abscess |  | Quinsy | J36 |  |

## 22. Skin Diseases

| # | Name | Short | Aliases | ICD-10 | Flag |
|---|---|---|---|---|---|
| 22.1.1 | Impetigo |  |  | L01 |  |
| 22.1.2 | Boils/Carbuncle |  | Furuncle |  |  |
| 22.1.3 | Cellulitis and Erysipelas |  |  | L03 |  |
| 22.2.1 | Herpes Simplex |  |  | B00 |  |
| 22.2.2 | Herpes Zoster |  | Shingles | B02 |  |
| 22.3.1 | Tineas |  |  | B35 |  |
| 22.4.1 | Scabies |  |  | B86 |  |
| 22.4.2 | Pediculosis/Lice |  |  | B85 |  |
| 22.4.3 | Tungiasis |  | Jiggers | B88.1 |  |
| 22.5.1 | Acne |  |  | L70 |  |
| 22.5.2 | Urticaria/Papular Urticaria |  |  | L50 |  |
| 22.5.3 | Eczema |  | Dermatitis | L20 L23 |  |
| 22.5.4 | Psoriasis |  |  | L40 |  |
| 22.6.1 | Leg Ulcers |  |  | L97 |  |
| 22.7.1 | Steven-Johnson Syndrome and Toxic Epidermal Necrolysis | SJS | TEN | L51 |  |

## 23. Oral and Dental Conditions

| # | Name | Short | Aliases | ICD-10 | Flag |
|---|---|---|---|---|---|
| 23.1.1 | Halitosis/Bad Breath |  |  | R19.6 |  |
| 23.1.2 | Dentin Hypersensitivity |  |  | K03.9 |  |
| 23.1.3 | Malocclusion |  |  | M26.4 |  |
| 23.1.4 | **!** Fluorosis |  | Mottling |  | code-text-unparsed |
| 23.1.5 | False Teeth |  | Ebinnyo |  |  |
| 23.2.1 | **!** Prevention of Dental Caries and Other Conditions Due to Poor Oral Hygiene |  |  |  | non-clinical-subject? |
| 23.2.2 | Dental Caries |  |  | K02 |  |
| 23.2.2.1 | &nbsp;&nbsp;↳ Nursing Caries |  |  |  |  |
| 23.2.2.2 | &nbsp;&nbsp;↳ Rampant and Radiation Caries |  |  |  |  |
| 23.2.3 | Pulpitis |  |  | K04.0 |  |
| 23.2.4 | Acute Periapical Abscess or Dental Abscess |  |  | K04.6 |  |
| 23.2.4.1 | &nbsp;&nbsp;↳ Post-Extraction Bleeding |  |  |  |  |
| 23.2.5 | Gingivitis |  |  | K05.0 |  |
| 23.2.5.1 | &nbsp;&nbsp;↳ Chronic Gingivitis |  |  | K05.1 |  |
| 23.2.6 | Acute Necrotizing Ulcerative Gingivitis/Periodontitis/Stomatitis | ANUG |  | A69.0 |  |
| 23.2.7 | Periodontitis |  |  | K05.2 |  |
| 23.2.8 | Periodontal Abscess |  |  | K05.21 |  |
| 23.2.9 | Stomatitis |  |  | K12 |  |
| 23.2.9.1 | &nbsp;&nbsp;↳ Denture Stomatitis |  |  |  |  |
| 23.2.10 | Aphthous Ulceration |  |  | K12.0 |  |
| 23.2.11 | Pericoronitis |  |  | K05.30 |  |
| 23.2.12 | Osteomyelitis of the Jaw |  |  | M27.2 |  |
| 23.3.1 | Oral Candidiasis |  |  | B37.0 |  |
| 23.3.2 | Herpes Infections |  |  | B00 |  |
| 23.3.3 | Kaposi’s Sarcoma |  |  | C46 |  |
| 23.3.4 | Hairy Leukoplakia |  |  |  |  |
| 23.4.1 | Traumatic Lesions I |  |  | S00.5 |  |
| 23.4.2 | Traumatic Lesions II |  |  |  |  |
| 23.4.3 | Traumatic Lesions III |  |  |  |  |
| 23.5.1 | Burkitt’s Lymphoma |  |  | C83.7 |  |

## 24. Surgery, Radiology and Anaesthesia

| # | Name | Short | Aliases | ICD-10 | Flag |
|---|---|---|---|---|---|
| 24.1.1 | Intestinal Obstruction |  |  | K56 |  |
| 24.1.2 | Internal Haemorrhage |  |  |  |  |
| 24.1.3 | **!** Management of Medical Conditions in Surgical Patients |  |  |  | non-clinical-subject? |
| 24.1.4 | Newborn with Surgical Emergencies |  |  |  |  |
| 24.1.5 | **!** Surgical Antibiotic Prophylaxis |  |  |  | non-clinical-subject? |
| 24.2.1 | Diagnostic Imaging: A Clinical Perspective |  |  |  |  |
| 24.3.1 | General Considerations |  |  |  |  |
| 24.3.1.1 | &nbsp;&nbsp;↳ General Anaesthesia |  |  |  |  |
| 24.3.1.2 | &nbsp;&nbsp;↳ General Anaesthetic Agents |  |  |  |  |
| 24.3.1.3 | &nbsp;&nbsp;↳ Muscle Relaxants |  |  |  |  |
| 24.3.3 | Selection of Type of Anaesthesia for the Patient |  |  |  |  |
| 24.3.3.1 | &nbsp;&nbsp;↳ **!** Techniques of General Anaesthesia |  |  |  | non-clinical-subject? |
| 24.1.1.1 | &nbsp;&nbsp;↳ **!** Techniques for Regional Anaesthesia |  |  |  | non-clinical-subject? |

## Needing a decision

| # | Chapter | Name | Reason |
|---|---|---|---|
| 1.2.1.4 | 1 | Rabies Post Exposure Prophylaxis | non-clinical-subject? |
| 1.2.1.5 | 1 | Rabies Vaccine Schedules | non-clinical-subject? |
| 1.3.1 | 1 | General Management of Poisoning | non-clinical-subject? |
| 2.1.5.2 | 2 | Cryptococcal Meningitis | duplicate-name:2.1.5.2,3.1.10.2 |
| 2.5.2.3 | 2 | Management of Complications of Severe Malaria | non-clinical-subject? |
| 2.5.2.4 | 2 | Malaria Prophylaxis | non-clinical-subject? |
| 3.1.4 | 3 | General Principles of Antiretroviral Treatment | non-clinical-subject? |
| 3.1.5 | 3 | Recommended First-Line Regimens in Adults, Adolescents, Pregnant Women and Children | non-clinical-subject? |
| 3.1.6 | 3 | Monitoring of ART | non-clinical-subject? |
| 3.1.8 | 3 | Recommended Second-Line Regimens in Adults, Adolescents, Pregnant Women and Children | non-clinical-subject? |
| 3.1.9.1 | 3 | Management of HIV-Positive Pregnant Mother | non-clinical-subject? |
| 3.1.9.3 | 3 | Care of HIV-Exposed Infant | non-clinical-subject? |
| 3.1.10.2 | 3 | Cryptococcal Meningitis | duplicate-name:2.1.5.2,3.1.10.2 |
| 3.1.11 | 3 | Prevention of HIV | non-clinical-subject? |
| 3.1.11.1 | 3 | Post-Exposure Prophylaxis | non-clinical-subject? |
| 3.1.11.2 | 3 | Pre-Exposure Prophylaxis | non-clinical-subject? |
| 3.2.3 | 3 | Pelvic Inflammatory Disease | duplicate-name:3.2.3,14.1.2 |
| 5.3.1 | 5 | Definition, Clinical Features and Diagnosis of TB | non-clinical-subject? |
| 5.3.2 | 5 | Management of TB | non-clinical-subject? |
| 6.1.5 | 6 | Diarrhoea | code-text-unparsed |
| 7.1.3 | 7 | Use of Medicines in Renal Failure | non-clinical-subject? |
| 11.2.1 | 11 | General Principles of Good Clinical Practice in Transfusion Medicine | non-clinical-subject? |
| 11.2.2.3 | 11 | Clinical Indications for Blood Transfusion | non-clinical-subject? |
| 11.2.3 | 11 | Adverse Reactions Following Transfusion | non-clinical-subject? |
| 11.2.3.1 | 11 | Acute Transfusion Reactions | non-clinical-subject? |
| 14.1.2 | 14 | Pelvic Inflammatory Disease | duplicate-name:3.2.3,14.1.2 |
| 15.1.1 | 15 | Provide Information about FP including Pre-Conception Care to Different Groups | non-clinical-subject? |
| 15.1.5 | 15 | Educate and Counsel Clients to Make an Informed Choice of FP Method | non-clinical-subject? |
| 15.1.9 | 15 | Manage Client for Chosen FP Method | non-clinical-subject? |
| 15.2.1 | 15 | Condom | duplicate-name:15.2.1,15.2.2 |
| 15.2.2 | 15 | Condom | duplicate-name:15.2.1,15.2.2 |
| 15.2.9 | 15 | Natural FP: Cervical Mucus Method and Moon Beads | non-clinical-subject? |
| 15.2.10 | 15 | Natural FP: Lactational Amenorrhoea Method | non-clinical-subject? |
| 16.1.2 | 16 | Management of Common Complaints during Pregnancy | non-clinical-subject? |
| 16.2.2.2 | 16 | Counselling for HIV-Positive Mothers | non-clinical-subject? |
| 16.4.8 | 16 | Care of Mother and Baby Immediately After Delivery | non-clinical-subject? |
| 16.4.8.1 | 16 | Care of Mother Immediately After Delivery | non-clinical-subject? |
| 16.4.8.2 | 16 | Care of Baby Immediately After Delivery | non-clinical-subject? |
| 16.5.2 | 16 | General Care of Newborn After Delivery | non-clinical-subject? |
| 16.5.3 | 16 | Extra Care of Small Babies or Twins in the First Days of Life | non-clinical-subject? |
| 16.6.1.1 | 16 | Postpartum Counselling | non-clinical-subject? |
| 17.1.2 | 17 | Assess for Special Treatment Needs, Local Infection, and Jaundice | non-clinical-subject? |
| 17.2.1 | 17 | Check for Very Severe Disease and Local Bacterial Infection | non-clinical-subject? |
| 17.2.2 | 17 | Check for Jaundice | non-clinical-subject? |
| 17.2.3 | 17 | Check for Diarrhoea/Dehydration | non-clinical-subject? |
| 17.2.4 | 17 | Check for HIV Infection | non-clinical-subject? |
| 17.2.5 | 17 | Check for Feeding Problem or Low Weight-for-Age | non-clinical-subject? |
| 17.2.5.2 | 17 | HIV-exposed Non Breastfeeding Infants | non-clinical-subject? |
| 17.2.6 | 17 | Check Young Infant’s Immunization Status | non-clinical-subject? |
| 17.2.7 | 17 | Assess Other Problems | non-clinical-subject? duplicate-name:17.2.7,17.3.9 |
| 17.2.8 | 17 | Assess Mother’s Health Needs | non-clinical-subject? |
| 17.2.10 | 17 | Counsel the Mother | duplicate-name:17.2.10,17.3.11 |
| 17.3.1 | 17 | Check for General Danger Signs | non-clinical-subject? |
| 17.3.2 | 17 | Check for Cough or Difficult Breathing | non-clinical-subject? |
| 17.3.4 | 17 | Check for Fever | non-clinical-subject? |
| 17.3.5 | 17 | Check for Ear Problem | non-clinical-subject? |
| 17.3.6 | 17 | Check for Malnutrition and Feeding Problems | non-clinical-subject? |
| 17.3.7 | 17 | Check for Anaemia | non-clinical-subject? |
| 17.3.8 | 17 | Check Immunization, Vitamin A, Deworming | non-clinical-subject? |
| 17.3.9 | 17 | Assess Other Problems | non-clinical-subject? duplicate-name:17.2.7,17.3.9 |
| 17.3.11 | 17 | Counsel the Mother | duplicate-name:17.2.10,17.3.11 |
| 17.3.12.1 | 17 | Feeding Recommendation during Illness | orphan-child non-clinical-subject? |
| 17.3.12.2 | 17 | Assessing Appetite and Feeding | orphan-child non-clinical-subject? |
| 17.3.12.3 | 17 | Feeding Recommendations | orphan-child non-clinical-subject? |
| 17.3.12.4 | 17 | Counselling for Feeding Problems | orphan-child non-clinical-subject? |
| 17.3.12.5 | 17 | Mother’s Health | orphan-child |
| 18.1.1 | 18 | National Immunization Schedule | non-clinical-subject? |
| 18.1.2 | 18 | Hepatitis B Vaccination | non-clinical-subject? |
| 18.1.3 | 18 | Yellow Fever Vaccination | non-clinical-subject? |
| 18.2.3.1 | 18 | Prophylaxis Against Neonatal Tetanus | orphan-child non-clinical-subject? |
| 18.2.4 | 18 | Vaccination Against COVID-19 | non-clinical-subject? |
| 19.1.1 | 19 | Infant and Young Child Feeding | non-clinical-subject? |
| 19.2.1 | 19 | Introduction on Malnutrition | non-clinical-subject? |
| 19.2.1.1 | 19 | Classification of Malnutrition | non-clinical-subject? |
| 19.2.2 | 19 | Management of Acute Malnutrition in Children | non-clinical-subject? |
| 19.2.2.1 | 19 | Management of Moderate Acute Malnutrition | non-clinical-subject? |
| 19.2.2.2 | 19 | Management of Uncomplicated Severe Acute Malnutrition | non-clinical-subject? |
| 19.2.2.3 | 19 | Management of Complicated Severe Acute Malnutrition | non-clinical-subject? |
| 20.1.1 | 20 | Notes on Use of Eye Preparations | non-clinical-subject? |
| 23.1.4 | 23 | Fluorosis | code-text-unparsed |
| 23.2.1 | 23 | Prevention of Dental Caries and Other Conditions Due to Poor Oral Hygiene | non-clinical-subject? |
| 24.1.3 | 24 | Management of Medical Conditions in Surgical Patients | non-clinical-subject? |
| 24.1.5 | 24 | Surgical Antibiotic Prophylaxis | non-clinical-subject? |
| 24.3.3.1 | 24 | Techniques of General Anaesthesia | non-clinical-subject? |
| 24.1.1.1 | 24 | Techniques for Regional Anaesthesia | non-clinical-subject? |

## Entries with no ICD-10 code in the source

203 of 470 candidates. The guideline
simply does not state a code for these; none has been inferred.


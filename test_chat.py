#!/usr/bin/env python3

from openai import OpenAI

import chat

context = """
A) Prostate, Right Base, core biopsy:
- Prostatic adenocarcinoma.
- Gleason score: 3+4=7
- 0.1 cm total cancer of 2.1 cm total core length, involving 1 of 2 cores
B) Prostate, Right Mid, core biopsy:
- Benign prostatic tissue.
C) Prostate, Right Apex, core biopsy:
- Benign prostatic tissue.
D) Prostate, Left Base, core biopsy:
- Prostatic adenocarcinoma.
- Gleason score: 3+4=7
- 0.8 cm total cancer of 2.5 cm total core length, involving 2 of 2 cores
E) Prostate, Left Mid, core biopsy:
- Prostatic adenocarcinoma.
- Gleason score: 3+4=7
- 1.4 cm total cancer of 2.2 cm total core length, involving 2 of 2 cores
F) Prostate, Left Apex, core biopsy:
- Prostatic adenocarcinoma.
- Gleason score: 3+4=7
- 0.3 cm total cancer of 2.9 cm total core length, involving 1 of 2 cores
G) Prostate, Lesion 1 (left base), core biopsy:
- Prostatic adenocarcinoma.
- Gleason score: 3+4=7
- 1.2 cm total cancer of 2.0 cm total core length, involving 3 of 3 cores
""".strip()

prompt = """
Extract the features from the pathology report
""".strip()

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_features",
            "description": """Get gleason score, stage, and other
            features from a prostate cancer pathology report""",
            "parameters": {
                "type": "object",
                "properties": {
                    "gleason_score": {
                        "type": "string",
                        "description": "The gleason score of the prostate cancer",
                    },
                    "diagnosis": {
                        "type": "string",
                        "description": """Histological diagnosis
                            of the prostate cancer. Choose acinar
                            adenocarcinoma for adencarcinoma not
                            otherwise specified""",
                        "enum": [
                            "acinar adenocarcinoma",
                            "ductal adenocarcinoma",
                            "transitional cell carcinoma",
                            "squamous cell carcinoma",
                            "small cell carcinoma",
                            "benign",
                            "other",
                        ],
                    },
                    "biopsy_location": {
                        "type": "string",
                        "description": "Anatomic location of the biopsy within the prostate",
                    },

                },
                "required": ["gleason_score", "diagnosis"],
            },
        }
    }
]


def test_chat():
    client = OpenAI()
    features = chat.get_features(
        client=client,
        context=context,
        prompt=prompt,
        tools=tools,
        model='gpt-4o',
    )
    for feature in features:
        print(feature)


if __name__ == '__main__':
    test_chat()

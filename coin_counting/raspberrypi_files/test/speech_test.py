import pyttsx3

textSpeech = pyttsx3.init()

totalOnePeso = 1
totalFivePeso = 3
totalTenPeso = 1
totalTwentyPeso = 55

def speakTotalCoins():
    global totalOnePeso
    global totalFivePeso
    global totalTenPeso
    global totalTwentyPeso

    parts = []
    if totalOnePeso != 0:
        parts.append(f"{totalOnePeso} 1 peso coins")
    if totalFivePeso != 0:
        parts.append(f"{totalFivePeso} 5 peso coins")
    if totalTenPeso != 0:
        parts.append(f"{totalTenPeso} 10 peso coins")
    if totalTwentyPeso != 0:
        parts.append(f"{totalTwentyPeso} 20 peso coins")

    if parts:
        if len(parts) == 1:
            text = f"You have a total of {parts[0]}."
        else:
            text = f"You have a total of {', '.join(parts[:-1])}, and {parts[-1]}."
    else:
        text = "No coins detected, please place some coins first."

    textSpeech.say(text)
    textSpeech.runAndWait()

while True:
    speakTotalCoins()
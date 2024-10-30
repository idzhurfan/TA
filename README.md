#NOTES
- Only .wav file can be used for DTMF Decrypt
- .wav DTMF file generated using third party software (like Cool Edit Pro 2.1)
- Cool Edit Pro 2.1 DTMF generate limited to 22kHz

Its a program that does encryption of text into ASCII types, so it can be used to generate DTMF (DTMF contain a tone number of 1234567890#*).
Current projects is using third-parties software of Cool Edit Pro 2.1 to generate the DTMF.

How to use :
1. Determine the text to be encrypted, put the text on Vig_Encrypt.py
2. The output should be an ASCII, it can be used to generate DTMF
3. Using DTMF generator (like Cool Edit Pro 2.1), generate the DTMF based on ASCII that have been created
4. Save the generated DTMF as .wav
5. To decrypt the .wav, use DTMF_Decrypt.py

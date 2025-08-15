from deep_translator import (GoogleTranslator,
                             ChatGptTranslator,
                             MicrosoftTranslator,
                             PonsTranslator,
                             LingueeTranslator,
                             MyMemoryTranslator,
                             YandexTranslator,
                             PapagoTranslator,
                             DeeplTranslator,
                             QcriTranslator)

# for translator in [ GoogleTranslator, ChatGptTranslator, 
#     MicrosoftTranslator, PonsTranslator, LingueeTranslator,
#     MyMemoryTranslator, YandexTranslator, PapagoTranslator,
#     DeeplTranslator, QcriTranslator]:
#     print()
#     print(translator.__name__)
#     try:
#         print(translator().get_supported_languages())
#     except Exception as e:
#         print(e)


sentences = [
    'The cat slept peacefully under the warm sunlight.',
    'He found a strange note hidden in the drawer.',
    'We watched the stars until morning slowly arrived.',
    'Her laughter echoed through the empty, quiet hallway.',
    'The old bridge creaked beneath the heavy wagon.',
    'They discovered fresh footprints in the wet sand.',
    'I forgot my umbrella during the sudden storm.',
    'The train vanished into the dark mountain tunnel.',
    'A small bird perched gently on the windowsill.',
    'She whispered a secret nobody else could hear.'
]

for i in range(len(sentences)):
    print(f'SENTENCE {i+1}: {sentences[i]}')
    print('Google:')
    print(GoogleTranslator("en", "cy").translate(sentences[i]))
    print("MyMemory:")
    print(MyMemoryTranslator(source="en-GB",target="cy-GB").translate(sentences[i]))
    print('\n\n\n')
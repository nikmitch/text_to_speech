# text_to_speech
OpenAI's TTS seems to have more natural voices than many reading apps I've found. Building a tool to download web pages and convert them to mp3 so I can listen to them on my phone later.

This involves stripping out all the html tags from the text, then removing all the bits that I'm unlikely to want to read (e.g. comments or links at the bottom of a blog post). I've found this to be a downside of current readers (e.g. @Voice reader) - they often read out parts that you wouldn't be focusing on if reading with your eyes. Rather than trying to define an explicit set of rules about what to exclude or include, I'm uploading that text to gpt-4o-mini (with a low temperature) to remove parts that I'm unlikely to want to read, which seems to work surprisingly well. 
(initial code, can convert to mp3 from url but splits into a new file every 4096 characters)

This code makes two calls to the OpenAI API - one to do the removal of unnecessary text, and another to do the actual text-to-speech conversion. Both of these will require an OpenAI API key, please see **INSERT LINK HERE** for instructions on how to get one **NB also add instructions on how to alter my code to put in your openai api key**. The text-to-speech part is pricier than standard text generation, at 1.5 cents per 1000 _characters_ (not tokens), so beware of your balance when converting large files. **Maybe put in an estimated cost function into the code somewhere?**

This is not super fast - the code seems to take about 30 seconds for 12k characters to do the removal of extraneous text, then 2 minutes for the conversion to MP3. **Track stats better later, put in standardised per 1,000 characters format**. So not great for real-time usage, at present it's more something you can get running with a few web pages you want to read, and come back later to transfer it to a mobile device.

Have run up against a 4096 character limit on the TTS, so the code splits these into separate files, then recombines them
On the combining front, I'm using ffmpeg, which can be downloaded from ffmpeg.org, or installed with conda through conda-forge using `conda install -c conda-forge ffmpeg`


Still to be added: 
- Making sure the files split at the end of a word rather than mid-word

# text_to_speech

### Overview

OpenAI's TTS seems to have more natural voices than many reading apps I've found. Building a tool to download web pages and convert them to mp3 so I can listen to them on my phone later.



### Skills demonstrated in this project

- Interacting with the OpenAI models (for text cleaning and text-to-speech)
- Ability to clean data, change formats (including e.g. stripping html tags), and manipulate multiple inputs and outputs
- Clean and readable coding

### How to use it

Clone the repo, open up `run_tts.ipynb` and alter the `url="www.example.com"` and `description_for_mp3_name='example_filename'` arguments of the `url_to_mp3()` function to be whatever url you want to get the text from, and the desired filename for the output mp3. You may also need to install packages 

The `url_to_mp3()` function is defined in tts.py, if you're curious to get a clearer step-by-step walkthrough of how it was developed, check out `tts_development.ipynb`

### How it works

This involves stripping out all the html tags from the text, then removing all the bits that I'm unlikely to want to read (e.g. comments or links at the bottom of a blog post). I've found this to be a downside of current readers (e.g. @Voice reader) - they often read out parts that you wouldn't be focusing on if reading with your eyes. Rather than trying to define an explicit set of rules about what to exclude or include, I'm uploading that text to gpt-4o-mini (with a low temperature) to remove parts that I'm unlikely to want to read, which seems to work surprisingly well. 

This code makes two calls to the OpenAI API - one to do the removal of unnecessary text, and another to do the actual text-to-speech conversion. Both of these will require an OpenAI API key, please see the [OpenAI quickstart guide](https://platform.openai.com/docs/quickstart) for instructions on how to get one **NB also add instructions on how to alter my code to put in your openai api key**. The text-to-speech part is pricier than standard text generation, at 1.5 cents per 1000 _characters_ (not tokens), so beware of your balance when converting large files. The code automatically produces an estimated cost for the text-to-speech part when running.

This is not super fast - the code seems to take about 30 seconds for 12k characters to do the removal of extraneous text, then 2 minutes for the conversion to MP3.  So not great for real-time usage, at present it's more something you can get running with a few web pages you want to read, and come back later to transfer it to a mobile device.

Have run up against a 4096 character limit on the TTS, so the code splits these into separate files, then recombines them
On the combining front, I'm using ffmpeg, which can be downloaded from ffmpeg.org, or installed with conda through conda-forge using `conda install -c conda-forge ffmpeg`.


### Possible future updates
- Making sure the files split at the end of a word rather than mid-word
- Might try switch this to a free/local version with allchat TTS ([LINK](https://www.youtube.com/watch?v=zdNHeKkG0xY)) -- could even get it to impersonate me or someone else!
- Allow file input to be a PDF (either at the url or locally uploaded)
- I should add a requirements.txt file to pip install all the necessary packages from and check it works in a fresh environment
- Add better tracking stats, put in standardised per 1,000 characters format
- Add functionality for uploading local files in general (.txt, .md, .pdf, .html?)
- Allow for extra instructions to be added at the end of the prompt (e.g. "in this pdf, I'm just interested in the segment starting from the Foreward and ending just before the bibliograpy")
- Allow user to manually specify a start string? And end string?? Provided they're unique, this could make sure you get exactly the segment you want
    - Maybe a preview functionality that shows the first few lines that will be included, and the last few lines? Then user goes continue Y/n based on whether that's correct
- Allow multiple URLs/files to be uploaded at once
- Turn into a web app somehow, to allow others to use it without running the python themselves?? Not sure how this would interact with the API key thing - don't want to give everyone my API key, but also shouldn't store theirs

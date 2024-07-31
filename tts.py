#!/usr/bin/env python
# coding: utf-8


# url = "https://importai.substack.com/p/import-ai-380-distributed-13bn-parameter"
# description_for_mp3_name = 'import_ai_380'
def url_to_mp3(url, 
               description_for_mp3_name, 
               delete_intermediate_files=True,
               text_to_speech_output_folder='text_to_speech_outputs'):


    # # Setup
    from openai import OpenAI
    import requests
    import os
    from bs4 import BeautifulSoup
    from pydub import AudioSegment
    from tqdm import tqdm


    # you'll need an openai api key to run this
    client = OpenAI()

    # Create the directory if it doesn't already exist
    if not os.path.exists(text_to_speech_output_folder):
        os.makedirs(text_to_speech_output_folder)
        print(f"Output directory '{text_to_speech_output_folder}' created successfully.")
    else:
        print(f"Output directory '{text_to_speech_output_folder}' already exists.")

 
    # First getting the html file from the url

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Get the HTML content of the page
        html_content = response.text
        print(f"getting html content from {url}") 
        print("HTML content saved to the variable 'html_content'.")

    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

    print(" ")

    # what's in the html_content variable is pretty unreadable - it has a bunch of html formatting stuff going on, which I don't want to hear when it's reading. Using bs4 to remove the formatting

    # Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract text and strip whitespace
    content_text = soup.get_text(separator='\n', strip=True)

    # # Print the cleaned text
    # print(content_text)


    # The above has gotten rid of the html stuff, which is great, but it also has a bunch of text from links at the bottom and top etc that I wouldn't want to read. I think this is a good use case for GPT4, so setting up a version of it with instructions to help me get rid of the parts that I wouldn't be interested in reading.
    # 
    # I found I had to tell it explicitly to NOT summarise or paraphrase at all, but it seems to do a pretty sweet job, especially after reducing the temperature to increase predictability

    print("Removing unnecessary headings and links from the text using GPT-4...")
    print(" ")

    text_for_reader_object = client.chat.completions.create(
    model="gpt-4o-mini", # "gpt-3.5-turbo" ran in about half the time, but it cut out the last paragraph
                         # "gpt-4" took 4x as long to run as the gpt-4o-mini model
    messages=[
        {"role": "system", "content": "You are an assistant who will help me out with cleaning up some text, so the relevant parts can be read out in a text-to-speech convertor. I have taken this text from a HTML file and removed all the tags. However, it still may have a bunch of headings and links that were in the orignal, but not of interest to someone reading the web page. Can you please remove the unnecessary headings and links from the text, so that the reader will just read what I want to hear? Make sure you include all relevant content from the whole document though. I DO NOT want you to summarise the text or change any of the words, outside of removing the headings and links. Please wrap the text in your output at 120 characters width"},
        {"role": "user", "content": f"Can please remove the unnecessary headings and links from this text {content_text}"}
    ],
    temperature=0.2 # I found that setting the temperature lower made sure that nothing was cut out of the text
    )

    text_for_reader = text_for_reader_object.choices[0].message.content

    # This is now in the format I want. I had a quick try at converting this into mp3 from here, but I've run up against a character limit of 4096. So I'm going to need to split my input up into a list of strings, convert them into mp3 individually, then look to concatenate them.
    # 
    # Note that the cost of the conversion isn't that cheap (1.5 cents per 1000 characters (USD)), so printing out expected cost here for user's awareness

    expected_cost_USD = len(text_for_reader)/1000*0.015  #cost 0.015 USD per 1000 characters
    print("Merging the MP3 files...")   
    print("")
    print(f"Expected cost of text-to-speech conversion: US${round(expected_cost_USD,2)}")

    def split_string(long_string, max_length=4096):
        # Create an empty list to hold the substrings
        result = []
        
        # Calculate the total length of the input string
        total_length = len(long_string)
        
        # Loop through the string and split it into substrings of max_length
        for i in range(0, total_length, max_length):
            substring = long_string[i:i + max_length]
            result.append(substring)
        
        return result

    # Split the text into parts of 4096 characters each
    text_for_reader_split = split_string(text_for_reader)

    # Print the result to check the output
    for idx, part in enumerate(text_for_reader_split):
        print(f"Part {idx + 1}: Length = {len(part)}")

    # Time to convert to an mp3 file! I'm enjoying the 'onyx' voice the most

    split_mp3_paths = []
    for i in tqdm(range(len(text_for_reader_split))):
        print(f"converting part {i+1} of {len(text_for_reader_split)}")
        response = client.audio.speech.create(
            model="tts-1",
            voice="onyx",
            input=text_for_reader_split[i]
        )
        
        split_mp3_name= f"{description_for_mp3_name}_{i+1}.mp3"
        split_mp3_path = os.path.join(text_to_speech_output_folder, split_mp3_name)
        response.stream_to_file( split_mp3_path )
        split_mp3_paths.append(split_mp3_path)
    print("finished saving all parts")
    print(" ")
    # print(f"saved mp3s: {split_mp3_paths}")


    # Next, want to merge these mp3s together back into one. To do this you need ffmpeg, which I installed with conda using `conda install -c conda-forge ffmpeg`. However, it can also be downloaded from ffmpeg.org if you're not using conda. 

    print("Merging the MP3 files...")
    print(" ")
    # Initialize an empty AudioSegment
    combined = AudioSegment.empty()

    # Loop through the list of MP3 files and append them to the combined AudioSegment
    for mp3_file in split_mp3_paths:
        audio = AudioSegment.from_mp3(mp3_file)
        combined += audio

    merged_mp3_path = os.path.join(text_to_speech_output_folder, f"{description_for_mp3_name}.mp3")
    # Export the combined AudioSegment as a new MP3 file
    combined.export( merged_mp3_path , format="mp3")

    print(f"MP3 files have been merged successfully! Final mp3 saved at {merged_mp3_path}")


    # clearing these files to save space
    if delete_intermediate_files:
        # Delete the intermediate MP3 files
        for mp3_file in split_mp3_paths:
            os.remove(mp3_file)
        print("Intermediate MP3 files have been deleted successfully!")


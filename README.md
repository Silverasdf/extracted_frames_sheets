# extracted_frames_sheets

This is a repo with my work with a UTK project.

## File Explanations

For those who are confused by some of the files, here is a brief explanation of what each file is:

- outputs/accuracy_matrices/* - These "accuracy matrices" show whether or not each image in each test in outputs/llava_prompt_engineering_trials/ matched the ground truth in accident_ground_truths.xlsx. 1 means that the particular question in the image matched the ground truth, 0 means that it did not.
- outputs/old_trials/* - Combination of OpenAI, Gemini, and LLaVA tests.
- outputs/llava_prompt_engineering_trials/* - Only the new LLaVA tests that I did after testing LLaVA initially. See llava_notes.md in that directory for more information. Most of these tests are for improving the prompt used.
- outputs/ground_truths/accident_ground_truths* - The ground truth for the accident questions in the LLaVA tests. It includes 200 sequences of images and answers to multiple questions about each sequence.
- commercial_llm_script.ipynb - This was the first file I used to test the accuracy of OpenAI/Gemini tests. API key needed in order for it to work
- accuracymatrices.ipynb - Prints results of an accuracy matrix
- llava-trials.xlsx - The excel spreadsheet I used to get the accuracy of the initial LLaVA test.
- combine_images.py - A script that takes a folder of images and combines them. Used for ground-truthing, fine-tuning and testing. Output is in outputs/combined_images/.
- parse_data.ipynb - Visualizes the data from each of the tests in outputs folder to make it more human-readable.
- llava_performance_analysis.ipynb - Analyzes the performance of the LLaVA time trials, which include performance information (how fast my machine can run the tests).
- performance_tests.ipynb - Analyzes the performance of the tests for the different models.
- llava_script.py - The script I used to run the LLaVA tests.

## My Experience

### The Dataset

My dataset involved sequences of images of car accidents. I use the concatenated_images directory by the end by using combine_images.py, but, of course, the dataset will start with the images in a directory. If you have videos, consider using ffmpeg to convert to a sequence of images.

```plaintext
dataset
    image1sequence
        1.jpg
        2.jpg
        ...
        n.jpg
    image2sequence
    ...
    imagensequence

concatenated_images
    image1sequence.jpg
    image2sequence.jpg
    ...
    imagensequence.jpg
```

### The Fine Tuning Process

Note that I reference my GitHub page (https://github.com/Silverasdf/extracted_frames_sheets), LLaVA's GitHub page (https://github.com/haotian-liu/LLaVA), and the LLaVA multi-image CLI GitHub Page (https://github.com/mapluisch/LLaVA-CLI-with-multiple-images). I used Google Compute Engine with 4 NVIDIA L100 GPU's. I have provided the environment.yml file that I used. Of course, anaconda is required to use the environment, but that can be installed easily by going [here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).

So, in order to start the fine-tuning process, I need to do two main things: Prepare the Image Sets and Prepare the JSON file.
In order to prepare the images, I used combine_images.py (my GH), and I copied the functions from the llava-multi-images.py (Multi-Image CLI GH) and then basically saved the image output to an output directory. I just ran my script with no arguments and modified the for loop range according to whichever extracted frames set I want to convert. This converts multiple images (all the images in the set) into one combined image to be fine-tuned with (in a grid-like formation, temporally sorted left to right then up to down).
In order to convert to the JSON format, I used automate_json_creation.ipynb (my GH). I followed the structure from the Finetune_Custom_Data.md file (LLaVA's GH) to make it. I just enumerated to get a unique id, but I think the rest is pretty straightforward. I paste the prompt exactly as I want it for the prompt and I paste the output of the ground truths excel sheet (converted into a CSV) into the answer section. No other input, other than the ground-truth csv file, is necessary.
From here, we have the images and the ground truths in the form of a JSON file. We can now move this into the VM to start fine tuning. To fine-tune, I cloned the LLaVA GitHub repository, followed their setup steps in their README, added the data and the json file under the "playground/data" directory, modifed finetune-lora.sh to fit our parameters, and ran sh finetune-lora.sh with no arguments.

Now, the fine-tuned model was saved into "checkpoints/model-name/". This includes only the fine-tuned weights. From here, you should combine the weights with the base model using the merge_lora_weights.py (LLaVA's GH) script with the recommended usage from LoRA.md (LLaVA's GH). (This is the script that is giving me errors. Technically, it can be skipped, as long as you specify the base model during evaluation, but every time the model is evaluated, it takes time to re-merge the weights).

Finally, I can run my evaluation script (script.py from my GH) to use the LLaVA CLI (from LLaVA's GH) with our desired input (the message and the images, combined into one image, using the same method as mentioned above, but instead, using the llava-multi-images.py file from the multi-image CLI GH page). I can, again, change the range of the for loop in order to pick which sets to evaluate on; however, I have been consistently using the first 100 sets from the dataset as our testing data. Now, all of our LLaVA output and performance information is found in an outputs directory. I, then, transfer that onto my local machine to manually test for accuracy.
To test the accuracy, I used parse_data.ipynb (from my GH) to more easily create my matrix of accuracies. This matrix compares the ground truth testing data to the output of LLaVA, and it's a list of 0's and 1's -> 0 means that it was wrong or not answered and 1 meaning it was right.

On this accuracy metric, we are focusing on every question individually, as some questions (binary yes or no) are more difficult to answer than others (specific accident type). A "1" represents the question being exactly right, while a "0" means there was an inaccuracy in the response to the question in some way. This metric was chosen to reduce the complexity of the output shown by the LLM; however, in this reduction, the accuracy metric does not show all the nuances that the LLM outputted.
After the matrix is created, I use performance_analysis.ipynb (from my GH) to create the plots that you saw in my initial presentation. This can be done with any of the accuracy matrices (which I have yet to create for the other 3 LLM's tested).

### The Commercial API Process

I used the commercial_llm_script with Google Colab. I also grabbed an OpenAI and Gemini API keys to use it. I then mounted the dataset to the Colab VM and ran the script.
Concatenated images are not necessary, as I the images directly into the commercial LLMs. I had to come up with the concatenate_images.py script when I found out that
LLaVA does not support multiple images.

## Results

### The Commercial LLM tests

The commercial LLM's were tested, and the results can be found in old_data/trials.xlsx. Overall, there were some solid results, where around 70% of the dataset was answered correctly. However, there were some questions that the commercial LLM's refused to answer

### Initial LLaVA Tests

Next, I used the LLaVA model to run initial tests, zero-shot. The results can be found in old_data/llava-trials.xlsx.

Also, I used the LLaVA model to run more tests, just using different tools such as prompt engineering, image shuffling, and other non-fine-tuning methods. The results and
a separate writeup can be found in outputs/llava_prompt_engineering_trials/llava_notes.md. From these tests, I was able to modify the prompt to get slightly better results, but not by much.

### Testing for Fine Tuning

For fine tuning, I ground truthed and processed 100 sequences of images. From here, we could convert the ground truths into a readable format for LLaVA and fine-tune the model.
After fine-tuning, I noticed that, unfortunately, the model was giving the same answer to every question, which implies that the model was not learning a general pattern.

As a result, I turned to a solution that involves getting a bigger and more diverse dataset. I worked with another research, Dr. Yangsong Gu, a post-doc from UTK, to get a
different dataset with better ground truths. He was able to provide many sequences of images, focused on the shoulder lane of highways. We fine-tuned the model on this
dataset, and the results were more accurate and diverse. However, the model was giving less detailed answers than a normal zero-shot LLaVA model. From here, we are looking to
convert the dataset ground truths (as in, the tabular data) into a more readable format for humans. This way, the model can give more proper answers to the questions.

### Papers and Testing for Performance

For the performance tests, please look into the outputs/comparing-llms directory for context!

First of all, to address the elephant in the room: Gemini and OpenAI, with no further prompt engineering, did not perform well at all. This is because of the extensive guardrails that existed during this test. Also, it seems that one error in an image will result in the model not working properly for the rest of the time, even though a new instance is created for every trial, just like the other LLMs that were tested. My theory is that there may be some hidden optimization done that cannot be seen or changed for this to occur. However, after lots of different prompts and manually stopping and starting the OpenAI model, [talk about Babita's confusion matrix here]. Our hypothesis is that Gemini, if given the same amount of time stopping and starting through the dataset and giving multiple prompts, will yield similar results to OpenAI's.

It is clear that LLaVA and VILA, the open source models, are comparable, though VILA seems to perform slightly better in areas such as fire, firetruck, and ambulance, while LLaVA performed better with type, police, and injury. VILA could not get a single accident type correct, and this is because it kept saying "traffic accident" or "traffic collision" without being specific.

As far as performances go, I wanted to only compare the total times, because we have all of the total times for each of the LLMs. Furthermore, I figured it would be useful to use box-and-whisker plots here, so that we can better see ranges of times. It is worth noting that VILA is the most consistent of the 4, and OpenAI has the biggest range of the 4. The open-source LLM's seem to be much more consistent and comparable to each other than their commercial counterparts.

I'm not sure how we would want to approach a conclusion section, but I do have a lot of things I've learned from doing these experiments that may be beneficial to others that want to repeat our process.

The consistent issue I get with the fine-tuning is the clear overfitting. Even if we provide 100 sequences, the model seems to find comfort in only answering one simple answer every time. My hypothesis for why this is has to do with our data not being of a high variety. Although we tried to mitigate this by only fine-tuning based on two accident types and then trying to see if it would choose either of the two, the model still wants to choose one accident type and stick with it. Furthermore, the data, as far as "Fire: yes/no" has an overwhelming ground truthed answer "no", which should make sense, as little accidents involve fires. However, this could mean that the model is fine-tuned to always say no to a fire. To mitigate this, we need exponentially more data to fine tune based on, and this may turn outside the scope of our research team.

## Future Work

My current plan for future work involved preprocessing both the tabular data and the image data before fine-tuning the model. I want to do some kind of "description" form for
the tabular data, so that the model will give a more detailed answer. This should not involve too much work. For the image data, my current idea is to use Facebook's Segment Anything model to only take the important parts of the image to sned in. After this, we can go through a normalization step and send it into the model to fine tune. These preprocessing techniques should, theoretically, be quicker, as we will need to preprocess any data that is given in real time. Another approach is to only preprocess the images
to fine tune them.

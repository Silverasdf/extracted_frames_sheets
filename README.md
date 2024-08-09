# extracted_frames_sheets

This is a repo with my work with a UTK project.

## File Explanations

For those who are confused by some of the files, here is a brief explanation of what each file is:

- outputs/accuracy_matrices/* - These "accuracy matrices" show whether or not each image in each test in outputs/new_llava_trials/ matched the ground truth in accident_ground_truths.xlsx. 1 means that the particular question in the image matched the ground truth, 0 means that it did not.
- outputs/old_trials/* - Combination of OpenAI, Gemini, and LLaVA tests.
- outputs/new_llava_trials/* - Only the new LLaVA tests that I did after testing LLaVA initially. See llava_notes.md for more information. Most of these tests are for improving the prompt used.
- 00000*.xlsx - A few trials I answered questions to frame by frame, rather than by each sequence of frames.
- accident_ground_truths.xlsx - The ground truth for the accident questions in the LLaVA tests. It includes 100 sequences of images and answers to multiple questions about each sequence.
- Accident_Tests.ipynb - This was the first file I used to test the accuracy of OpenAI/Gemini tests. API key needed in order for it to work
- accuracymatrices.ipynb - Prints results of an accuracy matrix
- llava_notes.md - Notes on what each of the new LLaVA tests do.
- llava-trials.xlsx - The excel spreadsheet I used to get the accuracy of the initial LLaVA test.
- make_movie.py - A script that takes a folder of images and makes a movie out of them. Used for ground-truthing.
- parse_data.ipynb - Visualizes the data from each of the tests in outputs folder.
- performance_analysis.ipynb - Analyzes the performance of the new LLaVA tests, which include performance information (how fast my machine can run the tests).
- script.py - The script I used to run the LLaVA tests.
- trials.xls* - The excel spreadsheets I used to get the accuracy of the OpenAI/Gemini tests. One has macros and one doesn't.

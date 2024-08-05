# New LLaVA Trials Notes

## Initial Tests

### Control Group

Prompt: Full test given, no shuffle, grid format, 2 types were in the prompt (T-bone, rear-end)

Conclusion: Unfortunately, the control group spit out the same results as the initial results, meaning that the initial additions to the prompt did nothing to improve the results. The accident type is still t-bone, and it says nothing else.

### More Accident Types

Prompt: Only accident type asked, multiple accident types were in the prompt (T-bone, rear-end, topple, spin-out, and more), grid format, no shuffle

Conclusion: LLaVA only spit out rear-end (the most) followed by T-bone (not accurate)

Some were left blank for unknown reasons.

### Accidents and vehicles

Prompt: Only accident type, no shuffle, grid format, multiple accident types were in the prompt (T-bone, rear-end, topple, spin-out, and more). Only difference from the last one to this one is the vehicle types involved were asked.

Conclusion: LLaVA only spit out rear-end (the most) followed by T-bone, and one front end collision. Comparing to the ground truth data, this is not accurate at all, given the majority of T-bone accidents in the dataset. LLaVA did not spit out the vehicles involved often at all, but when it did, it gave relatively correct answers.

Some were left blank for unknown reasons.

### Accident types

Prompt: Same as above, except only two types of accidents were asked: T-bone and rear-end

Conclusion: T-bone is primary answer, followed by rear-end, and nothing else was said. Furthermore, comparing to the ground truth data, the times when it would switch to rear-end were not accurate.

### No Accidents Listed (1 and 2)

Prompt: same as above, except no accidents were listed in the prompt, forcing LLaVA to give me the accident type on its own. Also, vehicle types were asked.

Conclusion: There is a lot of variety in the answers (more than anything else seen so far). However, the majority of the answers literally just said "car accident". That being said, when another variety was mentioned, it seems to be relatively accurate to the ground truths (at least, the ones I checked).

### No Example Inputs

Prompt: Same as above, but the full test was given

Conclusion: Same as above and from control group, just combined into one, basically.

### Number of Vehicles

Prompt: All I did was ask for the number of vehicles involved, but I told it that the same vehicle could appear in multiple images since it's a video.

Conclusion: LLaVA still, unfortunately, overestimates the number of vehicles involved in the accident.

### Full Test Shuffled

Prompt: Same as control group, but all images are shuffled, meaning that the cause and effect relationship should be non-existent to LLaVA.

Conclusion: Surprisingly, the results were the same as the control group. This means that the shuffling of the images did not affect the results at all.

### Shuffled Accident Types

Prompt: Same as No Accident Types, but images are shuffled.

Conclusion: The results were the same as the No Accident Types group, meaning that the shuffling of the images did not affect the results at all.

### Horizontal Images

Prompt: Same as No Accident Types, but instead of a grid like formation of the combined images, they are all shown in a horizontal line. To fix the resolution of the combined image, I needed to make sure there were less images, unfortunately. The idea here is that cause and effect would be more natural to LLaVA.

Conclusion: The results were about the same as the control group, meaning that the horizontal line of images did not affect the results at all. There could be a small difference in the number of vehicles involved, but it's hard to tell at first glance.

## After Initial Tests

### Full Test, New Prompt

Prompt: Full test given, no shuffle, grid format, a new prompt was given, where the model was told no accident types but also to give more details about the accident type.

Conclusion: The results were about the same as the control group combined with the results of the no accident types given, meaning that the new prompt, asking LLaVA to give more detail, did not affect the results significantly. The number of vehicles involved was still overestimated, but it does seem that the variety of answers was increased.

### Full Test, New Prompt, Shuffled

Prompt: Same as above, but all images are shuffled.

Conclusion: The results were about the same as the above, meaning that the shuffling of the images did not affect the results significantly.

### Full Test, New Prompt, Shuffled 2

Prompt: Same as Full Test, New Prompt, Shuffled. Doing this again just tests to see if anything changes from one exact test to another.

Conclusion: Same as above, meaning that doing the same test again did not affect the results significantly.

### Horizontal, Accident Types

Prompt: Horizontal images, accident types asked.

### Horizontal, Number Vehicles

Prompt: Horizontal images, number of vehicles asked.

### Horizontal, Shuffled

Prompt: Horizontal images, images are shuffled, full test done.

### Horizontal, Shuffled, Number Vehicles

Prompt: Horizontal images, images are shuffled, number of vehicles asked.

### Number Vehicles, Shuffled

Prompt: Grid-like format, number of vehicles asked, images are shuffled.

### Image Quality

Prompt: Just like the control group, except only the image quality is asked. LLaVA is asked to describe the image quality from giving a scale of 1 to 10. This is to help see if the image quality affects the results at all.

### One Image, Image Quality

Prompt: Same as Image Quality, but only one image is shown.

### New Prompt, Accident Types

Prompt: Accident types asked with the new prompt.

### No Accident Types (New prompt without "be specific"), Horizontal, Shuffled

Prompt: No accident types asked, horizontal image formation, images are shuffled.

### One Image, Accident Types

Prompt: Accident types asked, only one image shown. These one image tests are to see if LLaVA will say that no accident occurred, as the first image is not enough to determine that an accident occurred.

### One Image, Full Test

Prompt: Same as above, but the full test is given.

### One Image, Number Vehicles 1

Prompt: Same as above, but the number of vehicles is asked.

### One Image, Number Vehicles 2

Prompt: Same as above. I wanted to try this test again, since there were a few trials that were not answered, and I wanted to see if LLaVA would give me an answer this time.

## Test ideas

This mainly involves doing the same tests as above, but asking for the number of vehicles involved in the accident.

- One Image, but change the prompt to ask whether or not an accident occurred, so that LLaVA does not assume one way or the other.

## Conclusion (so far)

- It looks as though, if specifying more than just two types of accidents, it switches from primarily T-bone to rear-end, and sometimes front-end, but it does increase the variety of answers by a bit.
- Allowing LLaVA to choose the accident type on its own (no examples given) gives a lot of variety in the answers, but the majority of them are just "car accident". So possibly asking for more specific details about the accident type could help.
- LLaVA does not seem to care about cause and effect, as the shuffled images did not seem to affect the results at all, from first glance.
- We still need to figure out a way to get LLaVA to spit out the correct number of vehicles involved in the accident. It seems we have made progress on accident types by leaving it up to LLaVA, but the number of vehicles is still a mystery.

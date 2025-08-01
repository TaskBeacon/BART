# Balloon Analogue Risk Task (BART)

| Field                | Value                        |
|----------------------|------------------------------|
| Name                 | Balloon Analogue Risk Task (BART) |
| Version              | main (1.0)                          |
| URL / Repository     | https://github.com/TaskBeacon/BART  |
| Short Description    | A task measuring risk-taking behavior using the classic BART paradigm. |
| Created By           | Zhipeng Cao (zhipeng30@foxmail.com)   |
| Date Updated         | 2025/07/24                |
| PsyFlow Version      | 0.1.0                     |
| PsychoPy Version     | 2025.1.1                  |
| Modality             | Behavior/EEG                  |
| Language | Chinese |
| Voice Name | zh-CN-YunyangNeural |

## 1. Task Overview

The Balloon Analogue Risk Task (BART) is a computerized measure of risk-taking behavior. Participants are presented with a series of virtual balloons and must decide how much to inflate each one. For each pump, they earn a small amount of points. However, each pump also increases the risk that the balloon will pop. If the balloon pops, all points accumulated for that balloon are lost. The participant can choose to "cash-out" at any point, securing the accumulated points for that balloon and moving on to the next. The task uses different colored balloons (orange, yellow, and blue) to represent different risk levels (i.e., different probabilities of popping), which the participant must learn through experience.

This implementation uses the robust, predetermined explosion point method described by Lejuez et al. (2002).

## 2. Task Flow

### Block-Level Flow

| Step                       | Description                                                                 |
|----------------------------|-----------------------------------------------------------------------------|
| Load Config                | Load task configuration from `config/config.yaml`                          |
| Collect Subject Info       | Collect demographic/subject info using a `SubInfo` form                      |
| Setup Triggers             | Initialize trigger sender for EEG/fMRI (if applicable)                     |
| Initialize Window/Input    | Create PsychoPy window and keyboard handler                                |
| Load Stimuli               | Load all stimuli (images, sounds) via `StimBank`                           |
| Show Instructions          | Present text instructions explaining the task                              |
| Loop Over Blocks           | For each block: run a set number of trials, then show a break screen       |
| Show Goodbye               | Present final feedback with the total score                                |
| Save Data                  | Save all trial data to a CSV file                                          |
| Close                      | Close any open connections and quit PsychoPy                               |

### Trial-Level Flow

| Step                | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| Fixation            | Show a fixation cross for a brief period.                                   |
| Balloon Presentation| A colored balloon (blue, yellow, or orange) appears on the screen.          |
| Pumping Phase       | The participant can press the **spacebar** to pump the balloon, making it larger and increasing the potential score. With each pump, the risk of explosion increases. The participant can press the **right arrow key** to cash-out. |
| Outcome             | One of three outcomes occurs:                                               |
|                     | 1. **Pop:** The balloon explodes, and the participant loses all points for that trial. |
|                     | 2. **Cash-out:** The participant secures the points, and the trial ends.      |
|                     | 3. **Timeout:** If no response is made, the trial ends with no points.        |
| Feedback            | Feedback is shown indicating the outcome and points gained or lost.         |

## 3. Configuration Summary (`config.yaml`)

### a. Task Settings

| Parameter          | Value                      |
|--------------------|----------------------------|
| total_blocks       | 2                          |
| total_trials       | 10                         |
| conditions         | [blue, yellow, orange]     |
| pump_key           | `space`                    |
| cash_key           | `right`                    |

### b. Balloon Risk Profiles (Lejuez et al., 2002 method)

| Condition | `max_pumps` (Explosion Point Range) | `delta` (Points per Pump) |
|-----------|-------------------------------------|---------------------------|
| **Orange**  | 6 (High Risk)                       | 20                        |
| **Yellow**  | 12 (Medium Risk)                    | 10                        |
| **Blue**    | 24 (Low Risk)                       | 5                         |

### c. Stimuli

| Name                     | Type      | Description                                           |
|--------------------------|-----------|-------------------------------------------------------|
| fixation                 | text      | Central cross "+"                                     |
| `[color]_balloon`        | image     | Image of the blue, yellow, or orange balloon.         |
| `[color]_pop`            | image     | Image of the popped balloon.                          |
| pop_sound                | sound     | Sound played when a balloon pops.                     |
| cash_sound               | sound     | Sound played when the participant cashes out.         |
| instruction_text         | textbox   | Multi-line Chinese instructions for the BART task.    |
| block_break              | text      | Inter-block message showing block number and total score. |
| good_bye                 | text      | End screen showing the final score.                   |

### d. Timing

| Phase                 | Duration (s)        |
|------------------------|--------------------|
| fixation_duration      | 0.8                |
| balloon_duration       | 1.5 (Response window) |
| response_feedback_duration | 1.0              |
| feedback_duration      | 1.0                |

## 4. Methods

Participants performed a computerized Balloon Analogue Risk Task (BART) to assess risk-taking behavior. The task consisted of **2 blocks**, each comprising **5 trials**, for a total of **10 trials**. In each trial, participants were presented with a colored balloon (orange, yellow, or blue). They could repeatedly press the **spacebar** to inflate the balloon, accumulating points with each pump. The number of points earned per pump varied by balloon color. 

Crucially, each balloon had a predetermined, randomly selected explosion point, drawn from a uniform distribution specific to its color (Orange: 1-6; Yellow: 1-12; Blue: 1-24). If the number of pumps reached this explosion point, the balloon would pop, and all points for that trial would be lost. At any point before the balloon popped, participants could press the **right arrow key** to cash-out and bank the accumulated points. The primary dependent measures are the average number of pumps for non-exploding balloons of each color and the total score.

## 5. References

The task is based on the original design by Lejuez and colleagues:

> Lejuez, C. W., Read, J. P., Kahler, C. W., Richards, J. B., Ramsey, S. E., Stuart, G. L., ... & Brown, R. A. (2002). Evaluation of a behavioral measure of risk taking: the Balloon Analogue Risk Task (BART). *Journal of Experimental Psychology: Applied, 8*(2), 75–84. https://doi.org/10.1037/1076-898X.8.2.75

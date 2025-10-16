# Term Project

The term project will involve building a groundwater model of the Woburn site described in the book A Civil Action. We will divide the class into eight groups. Each group will build a MODFLOW model of the site and perform a particle tracking analysis. Two groups will represent Beatrice, two groups will represent the plaintiffs against Beatrice, two groups will represent W.R. Grace, and the final two groups will represent the plaintiffs against W.R. Grace. We will focus on one primary issue: flow paths and travel times. Using MODFLOW and MODPATH each group will attempt to prove or disprove that the hydraulic conditions were such that any TCE dumped at the sites could have reached the municipal water wells within the target time frame. At the end of the semester, each group will submit a written report and we will spend three days making presentations and debating the merits of each model.

Background slides: [woburn.pptx](woburn.pptx)

## Time Issues

The main focus of this project is to address the travel time issue. Using your model, you should be answering the question of whether or not TCE could have traveled from the W.R. Grace or Beatrice facility to wells G&H within the time frame addressed by the court trial. Consider the following comment regarding the jury instructions from Judge Skinner:

>>_"First: Had the plaintiffs established by a preponderance of the evidence that any of the following chemicals - TCE, perc, adn 1,2 transdichloroethylene - were disposed on the Beatrice land after August 27, 1968 (in the case of W.R. Grace, after October 1, 1964, and the date Well G had opened), and had these chemicals substantially contributed to the contamination of the wells before May 22, 1979? If the answer should be yes for one or more of the chemicals, then the second question: What, according to a preponderance of the evidence, was the earliest date - both month and year - at which each of these chemicals had substantially contributed to the contamination of the wells? And then: Had this happened because of the defendants' failure to fulfill any duty of care to the plaintiffs? Finally, if the jurors answered yes to that question, then this puzzler: What, according to a preponderance of the evidence, was the earliest time (again, both the month and year) at which the substantial contribution referred to in question 3 was caused by the negligent conduct of this defendant?" (Harr, 1995)_

Note that there is a specific time range mentioned by the judge. Refer to this time range as you discuss the results of your particle tracking analysis. The max travel time for the W.R. Grace case is about 14.5 years. For Beatrice it would be about 10.5 years. You may argue for applying a shorter time frame that this depending on your point of view. For example, these numbers represent the worst case scenario (the TCE was released at the earliest possible date).

## Web Site

The [Woburn Hydrogeology Data](https://woburn.readthedocs.io/en/latest/){target='blank'} web site has been established to provide you with data related to the Woburn site.  The data on this site are copies of actual investigations at Woburn. There may be more detail here than you end up using, but it is a good resource that you should explore carefully.

## Teams

The teams will be divided as shown in the following table. The group ids are shown in parentheses.

| W.R. Grace (1)   | 	Plaintiffs vs. Grace (2)        |
|:-----------------|:---------------------------------|
|                  |                                  |
|                  |                                  |
|                  |                                  |
| **Beatrice (3)** | 	**Plaintiffs vs. Beatrice (4)** |
|                  |                                  |
|                  |                                  |
|                  |                                  |

In terms of team management, I expect you to do the following:

1. Elect a team leader
2. Collectively draft a team contract that outlines who will do what. Each team member review and agree to the contract. You should upload your team contract to Learning Suite by the deadline shown in the table below.
3. Try to address participation problems within your group. Use the instructor as a last resort to arbitrate differences.

## Model

To support your viewpoint, you should first build a MODFLOW model. While the USGS model has been provided on the web site for informational purposes, you are not allowed to simply use the USGS model for your model. You need to build a model from scratch. Once you have your initial MODFLOW model built and running, you should then calibrate the model. Once you have calibrated the model and converted it to a predictive model, you can then proceed to the particle tracking analysis.

## Case Study Exercises

I have prepared a series of case study exercises that lead you through the process of building your model of the Woburn site. The purpose of these exercises is to show you how the model could be built. You are under no obligation to follow these steps exactly as you build your model. Feel free to improvise.

| Case Study	                                                                                                           | Notes                                                                                                                                            | 	Submission                                                                                                                                                                        |
|-----------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [Case Study #1 - Building the MODFLOW Model](https://byu-ce547.readthedocs.io/en/latest/termproject/casestudy1/case_study_1/) | 	Covers setting up the initial version of the model,<br> including the background image and conceptual<br> model.                                | 	Upload a *screenshot of the completed model<br> showing head contours.                                                                                                            |
| [Case Study #2 - Calibration](https://byu-ce547.readthedocs.io/en/latest/termproject/casestudy2/case_study_2/)        | 	Importing the head and flow observations and setting<br> up the calibration process.                                                            | 	Zip and upload a *screenshot of the calibrated<br> model showing the targets and a second<br> screenshot of the error norm summary.                                               |
| [Case Study #3 - Predictive Model](https://byu-ce547.readthedocs.io/en/latest/termproject/casestudy3/case_study_3/)   | 	Converting the model from calibration mode to forward<br> mode and splitting the model into three layers that<br> match the well screen elevtions. | 	Zip and upload 2-3 *screenshots of the multi-layer<br> model in oblique view with the cell faces turned<br> on. Include a screenshot showing the head<br> contours in plan view.  |
| [Case Study #4 - Particle Tracking](https://byu-ce547.readthedocs.io/en/latest/termproject/casestudy4/case_study_4/)  | 	Preparing the MODPATH options, importing property<br> boundary polygons and creating particle sets to<br> analyze travel times.                 | 	Zip and upload 2-3 *screenshots of your pathlines.                                                                                                                                |
| [Case Study #5 - Stochastic Analysis](https://byu-ce547.readthedocs.io/en/latest/termproject/casestudy5/case_study_5/) | 	Illustrates how to convert your particle tracking<br> model to stochastic mode in order to compute<br> probabilistic capture zones.             | 	(optional - no upload required)                                                                                                                                                   |
| [Case Study #6 - Transient Analysis](https://byu-ce547.readthedocs.io/en/latest/termproject/casestudy6/case_study_6/) | 	Describes how to convert your steady state model to<br> a transient model to simulate the seasonal variations<br> in pumping for wells G and H. | 	(optional - no upload required)                                                                                                                                                   |

_*Do not put the screenshots in a word document. Just zip up the image files (JPG, GIF, PNG)._

## Report

Each team will be required to submit a written report on the modeling project. I expect each report to be at least twenty pages long. At a minimum, you should describe the assumptions you made and the procedures you modeled in developing your model, you should describe the calibration process, the particle tracking results, and the conclusions you made. Be sure to present your results in relation to the [travel time question](https://byu-ce547.readthedocs.io/en/latest/termproject/tpoverview/tp_overview/#time-issues).

You will be given freedom to organize and format the report any way you wish. Your report should be as professional as possible. The report should be prepared and uploaded in **MS Word** format.

Please write your report in **first person narrative.** For example, instead of saying "the model was then calibrated", you should say "we then calibrated the model".

## Presentation

Each group will be given part of a class period to make an oral presentation of the results. This will take two periods.

For the presentation, I would like you to prepare a PowerPoint presentation. Upload your Powerpoint by the deadline so that I can make sure it is set up properly.

Make your presentation last 15 minutes. This will leave a few minutes for Q/A.

## Grading

The term project is worth 22% of your grade. I will assign a grade to each team based on my evaluation of the written report and the oral presentations. The term project score is broken down as follows:

### 1) Model development milestones (15%)

Please keep in mind the following milestones. For each item, the completed item (document, spreadsheet, etc.) should be uploaded into Learning Suite. See the schedule for due dates.

| Part  |      	Value       | 	Item Due                                      |
|:-----:|:-----------------:|:-----------------------------------------------|
|  a.   |      	3 pts       | 	Team contract                                 |
|  b.   |      	3 pts       | 	Working flow model (case study #1)            |
|  c.   |      	3 pts       | 	Calibrated flow model (case study #2)         |
|  d.   |      	3 pts       | 	Predictive model (case study #3)              |
|  e.   |      	3 pts       | 	Particle tracking analysis (case study #4)    |
|  f.   |      	73 pts      | 	Written project report                        |
|  g.   |      	12 pts      | 	Oral report                                   |

All items should be uploaded by due date shown using Learning Suite.

### 2) Oral report (12%)

Presentations should be professional, informative, and cover the basic features of your project. Keep your introductions brief since we are all quite familiar with the background information on the Woburn case. Make sure you cover all of the primary assumptions you made when building the model. Explain your calibration results and the results of your particle tracking analysis. Describe any special types of analysis that you considered.

### 3) Written report (73%)

a) Quality of writing, graphics, and organization (23 pts)

Be sure to proof several times to remove spelling and grammar errors. Assume your audience is familiar with groundwater modeling but don't assume that they are experts on the GMS interface. In other words, don't spend time explaining details unique to GMS such as what coverages you used, what menu commands you selected, etc.

b) Completion of basic modeling steps required (18 pts)

Be sure to fully document what you did and the assumptions you made. Include a full set of error norms for your final calibrated model. Also be sure to list/graph your final optimal values for recharge and K.

c) Thoroughness and rigor with respect to exploration and analysis of model results (32 pts)

In this case I am looking to see what you did to explore your model once it was constructed. How thoroughly did you investigate the particle tracking results? This includes (but is certainly not limited to) how you dealt with modeling assumptions such as recharge, the manner in which you analyzed your calibration results, how you selected your ranges and starting values for parameters, sensitivity analyses, risk assessment (stochastic analyses), transient factors, etc.



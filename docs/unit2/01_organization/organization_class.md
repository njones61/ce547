# Mountain-Lake Model

Consider the following site:

![mtn_range.png](images/mtn_range.png)

Build a simple groundwater model representing this system. Input is from recharge. Parallel flow boundaries on the top and bottom.

1. Build grid
>a. X, length = 20000, 100 cells<br>
>b. Y, length = 15000, 75 cells<br>
>c. Z, length = 500, 1 cell<br>

2. Properties
>a. Top = 3200, bottom = 2700<br>
>b. K = 2 ft/day<br>

3. Recharge
>a. 20 inches of rain per year<br>
>b. 15% reaches aquifer

4. Lake
>a. Specified head<br>
>b. Elevation = 3000

5. Save and run model<br><br>
6. Add a well
>a. Permitted at 10 AFA (acre-ft/year)

7. Explore
>b. Pumping rate (bigger)<br>
>c. More wells<br>
>d. K value<br>
>e. Recharge

## Solution

<details>
<summary>Click here to see calculation details:</summary>

<br>

<strong>Recharge:</strong><br>
• 20 inches of rain per year<br>
• 15% reaches aquifer<br>
• 20/12*0.15/365=0.0006849315 ft/day<br>

<br>

<strong>Well:</strong><br>
• Permitted at 10 AFA (acre-ft/year)<br>
• 10*43560/365 = 1193.4 ft^3/day<br>

</details>

<br>
Video: [<u>www.youtube.com/watch?v=4sy4xoizQso</u>](https://www.youtube.com/watch?v=4sy4xoizQso)
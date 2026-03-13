# Project and Schedule
## Requirements
We need to create **UiPath** compatible *object repository* which **UiPath Studio** do manually by selecting each ui element. The process should be automated in our module. \
*```Object Repository must be runnable in the UiPath Studio.```*

---
## Solution Proposal
### Step-1: UI Element Detection
Firstly we need to indentify each Ui element for example:
 - Text Field
 - Button
 - Radio Button
 - Check box
 - Clickable Link

Two approach we can consider:
1. **Computer Vision (YOLO)**: We will pass each page screenshot then our model will detect each **UI Element**. This probably takes time to solve some challenging task like dataset collection to train the model. And Firstly we need to store all screenshot of the full website (SAP).
2. **Testing Automation Library (Selenium)**: Since **Selenium** provide a lots of functionaly like Document Object Model (**DOM**) parsing on the live web page, take screenshot, store clickable region, so we can take lot of advantages from it. So, to reduce complexity and time constraint we can use selenium to surve our purposes. Selenium can easily detect **UI Element** with proper anchor box and able to define the **UI Element** type.


### Step-2: Find Sequence of Operation
Suppose, we have to sign in a page and enter the home page. So, we must ensure the operation sequence. 

**Example-1: Sign Page**\
```ENTER USER NAME --> ENTER PASSWORD --> SUBMIT ```

**Example-2: Form Fill UP**\
```ENTER FIRST NAME -> ENTER LAST NAME -> ENTER ADDRESS -> ENTER PHONE NUMBER```

So, we must maintain a separate file to fillup form sequence.

### Step-3: Input Data
Sometime, we need to fill up form with some data. So, we can maintain a separate file to store input data for each form field.

### Step-4: Traverse Each Page
Since, we have clickable item links (Got from selenium) and sequence of operation, so we can easily traverse each page by clicking on the clickable item link and fill up form with input data.

### Step-5: Generate Object Repository
Finally, we can generate object repository in **UiPath** compatible format. We can use **XML** or **JSON** format to store the object repository for each page. This object repository can be easily imported in **UiPath Studio**.

# EE4-PostBotPat
HCR Coursework 2018

## Deadlines
- 1/11: Design Report
- 29/11: Individual Demo
- 13/12: Final Demo
- 20/12: Final Report

## Project Phases
- Phase 1: Can deal with medium sized packages, one person at a time, people only come when they have a package, printed labels. One package per person only.  
- Phase 2: Can have people arrive even if they don't have a package.
- Phase 3: Multiple packages per person allowed.
- Phase 4: Allow for more package sizes.

## Workflow
- New work (features, bug fixes etc.) begins life as an issue (e.g. implement time prediction for pick ups, fix mistaken identity bug).
- New code / assests are created in dev branches.
- A merge request is then opened to merge the dev branch into the integration branch.
- The integration branch is tested and evaluated.
- If testing is successful then the integration branch is merged into master and the issue is closed.

## Code Style Guide

Writing good code is a good thing. Pat needs good code, otherwise he probably won't function properly. Here are some things that are good practice to adhere too- don't just do it for yourself, do it for Pat.

The main assumption here is that we all have good knowledge of good coding practice (use of header files, using OOP when there needs to be OOP etc) and so this is just a quicker guide to make sure that everything works as best it can and avoid any obvious mistakes that come about from composition.

### Function Names 

Function names should start with capital letters and describe exactly what the function does in as few words as possible, but with sufficient detail, for example:
```C++
void MovingPatsRightArm{};
```

Shortening words is also good, for example
```C++
void InitPat{};
```

In some cases, a sub-system such as a camera or sensor may require a number of routines that are then exposed through an API that you have written. In this instance, it's good practice to pre-append the name of that device to the function routine, for clarity and to avoid confusion with other sub-systems, like:
```C++
Kinect_InitIRSensor{};
...
codey codey codey;
...
Webcam_Init{};
...
```

### Class and Variable Names

Variable names are dependent on the scope of the variable and should define what they are used for. Single letter names, such as the ever classic `i` `j` and `k` should be restricted to the use of one time (in a function) indexers only. 

Global variables should be named as such:
```C++
uint8_t g_patmovecount;
```

Local variables should not have the same name as globals (unless you want to be brave and take a chance with how different compilers deal with scope, but that's for a talk over a beer). They don't need a pre-appended label to denote that they are local, so should be named like:
```C++
uint8_t throwawayaccumulate = 0;
```

In the case of class names should be treated as proper nouns. Member variables should indeed denote that they are variables that can change the state of an object. This is achieved with pre-appending `m_` to the variable name, and is done as simply as:
```C++
class Pat
{
public:
  void Pat{};
  void Pat_Init{};
  ...
private:
  uint8_t m_handlocation; // <-- member variable here
  ...
}
```

### Use of Braces

Due to popular demand, the following bracing style is to be used:
```C++
if(condition){
  ...
  codey codey codey;
  ...
}
```

While on the subject, tabs should be **four** spaces. 

### Use of Global Variables

Global variables should be used sparingly. They ideally should only be used when data needs to be shared between modules such as interrupts or when state information outside of objects should be saved. 

### Object Oriented Code and use of Virtual Functions

Virtual functions probably don't need to be used in PostBot Pat. However, if you find yourself needing to use it, be strict with yourself and determine where you need concrete inheritance and where `virtual` may come in useful.


### Generic Types

Where possible, it's better to use generic types. C++ 14 and C++ 17 have extensive support for this and it really helps to extend the code's readability and operability. For these types, the following convention should be used:
```C++
template<class t_PatTemplate>
...
etc
```

### Namespaces 

Namespaces are very useful indeed. They can be used to separate code and make names explicit. I'd recommend using them, but it's not the end of the world if we don't.














=======
## How to run the Baxter simulation

In 2 terminal tabs, run:
```
cd ~/ros_ws

./baxter.sh sim
```

In the 1st tab, run:
```
roslaunch baxter_gazebo baxter_world.launch
```

The gazebo terminal window should open with the robot in the world.

Then, in the 2nd terminal tab:
```
rosrun baxter_tools enable_robot.py -e
```

You can now run python scripts to move Baxter and see it in the gazebo simulator. For example:
```
rosrun baxter_tools tuck_arms.py -t
``

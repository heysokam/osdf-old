# TL;DR
## Must have  
```md
- Keep track of your changes. ALWAYS.  
- Document. ALWAYS. And Excessively.  
- Not everyone understands what you are doing, and/or doesn't remember  
- Old code modifications  
  Keep track of old code modifications with `//::OSDF yourname->key : description`.  
- New code  
  Can be tracked with git history, patchnotes, etc.  
```
## Styling  
```md
- Categorization is always first  
- One Gigantic File/Folder to rule them all  
  Categorize with folders. A complex system needs a complex folder structure for intuitive navigation.    
  Trying to hide complexity only makes the problem worse.     
- Word order: Idiomatic vs Categorical  
  Category -> Thing -> Differentiating Exception   
  Names such as: `trgBuild_init()`     and `trgBuild_update()`  
  Instead of:    `init_build_target()` and `update_build_target()`  
- Standard C99 
  Variables are defined where they are first used, not at the top.  
  Don't use one letter sentry variables outside of their loops. Find a way around them. 
  If you need them mandatory, they MUST have a unique and self-explanatory name!  
```
```md
- Compact, but Intuitive Wording
  Compact code is desirable. But compactness can reduce readability. Understand and use its rules.
- 1 letter words are extremely undesirable
  2 letter words are slightly better, but not by much.
- 3 letter words are immediately project wide language
  If you name something `trg`, referring to `target`, it MUST mean target **everywhere else** in the project. 
  This includes multiword names, such as `trgBuild`.
  They are very desirable, but slightly harder to work with.  
- Word shortening is the preferred way to name
  `QuatMul(q1, q2);` is much better than `QuaternionMultiply(quat1, quat2);`
- Verbose wording is extremely undesirable, and will ALWAYS be rejected
  Use comments and a smart naming scheme with shorter names for expressing ideas, not verbosity.
- Case styling: New code  
  camelCase preferred   
  PascalCase for types and constants  
  snake_case discouraged
  SCREAMCASE should be avoided. Use PascalCase with good names
- Case styling: Old code  
  Respect original Q3 code formatting when editing in-place.    
- General styling  
  Project loosely follows NEP1 formatting guidelines (with 2x line width)  
```
```md
- Others:  
  Use the project's `.clang-format` file only for new code for now.  
- One line, one idea  
- Line size  
  A screen that can contain more than 150 or 160 characters easily with huge characters. Don't restrict it to 80.  
- Line breaks  
  Keep the code into one line where possible. Unless you are expressing more than one idea.  
- Tab size  
  Indentation width of 2 spaces for all new code. No tabs.  
  Keep old code the same for now.  
- Everything else:
  Use the `.clang-format` file.
```

--- 
Details and reasoning:

# Must haves
## Keep track of your changes. ALWAYS.
In this engine, changing one thing usually requires modifying 3-4 different code files minimum.  
And the engine is very difficult to navigate, so changes can get lost really easily.  
As such, you should ALWAYS keep track of what files you have modified, and why.  

You might think "I know how this works, I don't need this"... but you will be surprised how much you will regret that.   
And if you actually have such elephant memory and really don't need it ever, you will be making life miserable for the next person that comes after you.  
Because the person won't just be dealing with your code. They will be dealing with your code AND the engine's code.  
And yours might be simple, but the engine isn't. At all.  

## Document. ALWAYS. And Excessively.
Like the previous paragraph implies, this engine can be an absolute B to work with.  
Assuming that you wrote this code, it would take you literally two seconds to turn this:  
```c
// Code from:   src/engine/rendc/tr_font.c
buffer = ri.Malloc(width*height*4 + 18);
Com_Memset (buffer, 0, 18);
buffer[2] = 2;    // uncompressed type
buffer[12] = width&255;
buffer[13] = width>>8;
buffer[14] = height&255;
buffer[15] = height>>8;
buffer[16] = 32;  // pixel size
```
Into this instead:  
```c
// TGA header indexes
#define TGA_DATATYPECODE 2
#define TGA_WIDTH_B1 12
#define TGA_WIDTH_B2 13
#define TGA_HEIGHT_B1 14
#define TGA_HEIGHT_B2 15
#define TGA_BITSPERPIXEL 16
//.......................
#define TGA_HSIZE 18
//.......................
const int    colorChannels = RGBA;
const size_t bufsize       = width * height * colorChannels + TGA_HSIZE;
byte*        buffer        = malloc(bufsize);  // alloc enough memory for the tga image
memset(buffer, 0, TGA_HSIZE);                  // Set all bytes of the buffer header to 0
buffer[TGA_DATATYPECODE] = 2;                  // uncompressed type
buffer[TGA_WIDTH_B1]     = width & 255;        // First byte of width
buffer[TGA_WIDTH_B2]     = width >> 8;         // Second byte of width
buffer[TGA_HEIGHT_B1]    = height & 255;       // First byte of height
buffer[TGA_HEIGHT_B2]    = height >> 8;        // Second byte of height
buffer[TGA_BITSPERPIXEL] = 32;                 // pixel size
```
What changed in code behavior? ... Nothing. Semantics.  
But the code is now documented, instead of requiring everyone that works with it to do the whole process of analyzing the code step by step, searching for the TGA header file specification online, decrypting what the code was meant to do in the first place... or instead just skip the whole thing entirely and having to wing it because it just takes too much time to deal with the unnecessary complexity.  

This engine has enough of this BS for a couple hundred lifetimes. **Don't make it worse.**  
Document. ALWAYS. And do it excessively.  

## Not everyone understands what you are doing, and/or doesn't remember
Not everyone has such memory, or such good logical deduction skills, that they won't need comments ever.   
This engine is extremely guilty of this mentality.  

This project, instead, is built assuming that the person reading has no memory of what the code does.  
You should respect that. Always.  

The engine has hundreds of thousands lines of code written without respecting this at all.  
Don't make this even worse than it already is.  
Explain what everything in your code does. It takes two minutes to do it in place, and hundreds of hours to do it "later"  
_(read as: never actually do it because its a gigantic pain in the ass)_.  

The reader might have forgotten _(or be new, and really really need the explanation)_.  
Always document, and assume nothing.  

## Old code modifications
For keeping track of old code modifications, the project uses `//::OSDF keyword`.
If you search for `//::OSDF` you will find all code modifications that the mod has done to the original q3a code
For multiline changes, these blocks always end with `//::OSDF end`
All other changes always start with `//::OSDF keyword`. 
- `modded` or `change` means something was modified, but overall behavior will be similar
- `added` means it is new code that didn't exist before in q3a
- `removed` this is not needed much, but self explanatory. Only used in cases where we want to keep track of removed code, but still keep using parts of the original. Very undesirable, so please avoid. If a change is big enough, it is preferable to hardwire the old code into a new codeflow, than to modify the original code in place _(see the hook towards `phy/*` code inside `bg_pmove.c` `Pmove()` for an example)._

Please avoid old code modifications where possible. But if you must modify, then add your name to the changes somewhere, in the format: `//::OSDF name->key : explanation`. _Valid keys are the same as the patchnotes format. `chg`, `fix`, `add`, etc. See the patchnotes file for a list of options._   
Example:   
```c
//::OSDF sokam->add  : Added thing and otherThing, because they were missing
thing();       // Has new super important code. Read documentation inside the function
otherThing();  // Also has some new code that is needed to make X and Y work
//::OSDF end
```
```c
someOtherCode();  //::OSDF sokam->chg  :  Switched oldCode with someOtherCode
```
Also, avoid keeping duplicates in commented out code.  
Document your change properly, and rely on your explanation, patchnotes and git history to find the old outdated code.  
Duplicated commented out code everywhere, plus a complex codeflow, will turn any codebase into a mess. And this engine is already difficult enough to follow. We don't need any more of that.  

## New code
New code doesn't have such strict requirements for code modification as the above, **as long as the code is contained in non-q3a files**.  
As you can imagine, using the above ruleset will result in code files filled with `name->new` all over, which makes no sense for newly written code.  
For simplicity, new code (that uses separate files) can be tracked with other methods (git history, patchnotes, etc).

The reason such rules exist for the old code is because keeping track of whats new and what was originally there can be an absolute nightmare. And, as was mentioned before, the code is already hard to work with. So any way to make that better is gonna be very impactful.

An example of the new code system can be found in `src/game/sgame/phy/*`.

# Styling
---
## Categorization is always first
_This section uses concepts from Jungian Psychology._  
_Search for `Ne/Si vs Ni/Se` or `Jungian Cognitive functions` if you want to understand the whys of what is said here._   
_It's not just some rando's opinion._

### One Gigantic File/Folder to rule them all
Some people really believe in this mindset.  
They believe it makes them faster, and they understand things better with this system.  
Celeste devs really believed in this. And created their infamous 15k loc player controller file.
John Carmack also believed this, and structured q1 into one gigantic folder, and q3 with gigantic files instead.

But not everyone's brain works like that. For me (sokam), for example, gigantic files/folders are an absolute nightmare to navigate and work with.  

```md
I don't want to invest the time to categorize this project more in depth, so I won't.
```
Very understandable, when your brain can improvise better than categorize. But horrible for the opposite type of person. 
_(In Jungian Psychology words: strong Ne and therefore weak Ni)_.  

```md
I can remember how everything is named in this file/folder. Why separate it, when I can search instead.
```
Great if you have good memory, and terrible if you are part of the % of population whose memory is akin to that of a goldfish.  
_(In Jungian Psychology words: strong Se and therefore weak Si)_

Categorization is very important for higher level analysis of a project _(Ni)_.  
It is unnecessary if you are the type of person who just "wings it" _(Ne)_, have good memory _(Si)_, and don't need higher level analysis much _(Ne)_. But for some people, that's just not feasible. Not everyone's brain works in the same way.  

If you open a folder and don't see words (aka folder names, categories) that lead you to where you want to go, you will need to spend a big chunk of time figuring out -where- to go to even start. And then repeat that pattern constantly in your workflow, when you could just navigate with the guidance of categorization, and invest the extra time into extra code (instead of into extra project navigation or file searching).
IDE's make navigation easier. But IDE's don't give you the higher level context of how things work. Categorization does.

Folder names should explain the big picture idea of what the code contained does.
`cl_draw.c` is such a category, yes... but its too shallow.
It doesn't really tell you what the file is actually doing, only that it's part of the client and it draws. And it will also be lost in a sea of files sorted alphabetically. 
So you will need to open the file, read it, and probably a couple other more, until you find the one you actually needed instead. Wasted time for no benefit.  

`client/render/utility/draw.c` would be a better example of how to categorize the exact same idea, but with more depth.  
If I'm looking for something in the renderer, that's not utility, I won't even see the draw file. And I don't need to. _(less noise, faster navigation)_.  
And if I'm looking for the drawing file, it would take me just a quick skim to find the folder, because the names/categories guide me towards it.

And that's without mentioning encapsulation, which can only done through file separation in C.

TL;DR:
Categorize with folders. A complex system needs a complex folder structure for intuitive navigation.  
Trying to hide complexity into one-file or one-folder structures only makes the problem worse.   
Specially in the complexity of a Carmackian engine.  

### Word order: Idiomatic vs Categorical
This project follows categorical naming, and not idiomatic english ordering.
```
Category -> Thing -> Differentiating Exception 
: catThing_exc
```
This creates names such as: `trgBuild_init()`     and `trgBuild_update()`
Instead of the idiomatic:   `init_build_target()` and `update_build_target()`

### Standard C99 
Variables are defined where they are first used, not bunched up at the top.  
Don't use one letter sentry variables outside of their loops. They are unsafe and confusing. Find a way around them. 
If you require one of those, then you are not using a sentry variable anymore. Therefore you MUST give it a unique and self-explanatory name, just like with any other variable.  

### Compact, but Intuitive Wording
Compact code is desirable, since its faster to read.
But compactness can reduce readability real fast. As such, it has some important rules attached.  

- 1 letter words are extremely undesirable
Unless it is painfully obvious what the variable is doing.
_r referring to result/return in a short function_
2 letter words are slightly better, but not by much. Both of them should always be commented to avoid confusion.

- 3 letter words are immediately project wide language
If you name something `trg`, referring to `target`, then that shortening MUST mean target **everywhere else** in the project. Not just in your code.  
This includes words that are part of multi words _(such as trgBuild, where trg must also mean target)_  
They are slightly harder to work with, but very desirable.

- Word shortening is the preferred way to name
`QuatMul(q1, q2);` is much better than `QuaternionMultiply(quat1, quat2);`
The engine sure has a lot of examples of the latter, but please remember word shortening for new code.
And, at all costs, avoid pure verbosity.

- Verbose wording is extremely undesirable, and will ALWAYS be rejected
Use comments and a smart naming scheme with shorter names for expressing ideas, not verbosity.
```c
void ThereIsAbsolutely(NoReasonToWrite* NoReason_ForCodeLikeThis, InThisEngine ThisEngine_sinceTheCode) {
  Code_wontEverBeModifiedBy(NonProgrammers);
}
// If you think this example is obnoxious/ridiculous, you would be surprised of what I've found in user-facing production code before :facepalm:
```
```c
// Use shorter names, a smart naming scheme and good comments to explain them
// This type of code can become self explanatory, cleaner, more readable and faster to work with,
// than what verbosity alone can ever achieve. Plus verbose code is both slower to read and write.
void func1(Type* var1, Type2 var2) {
  func2(var3);
}
```

### Case styling: New code
camelCase preferred 
PascalCase for types and constants
snake_case discouraged, only for category exception management (`_init` and `_update` are examples of such exceptions).
SCREAMCASE should be avoided. Use PascalCase with good names instead

### Case styling: Old code
Respect original Q3 code formatting when editing in-place.  
Unless the code is contained inside a new function, in which case use the styling you find appropriate for that function (either old or new).  
In an ideal world, the whole engine would follow New Code rules. But we are not there yet.  

### General styling
Although its written in C, this projects roughly follows NEP1 formatting guidelines 
_(except 2x line width, and a couple other exceptions covered by the .clang-format file)_

### Others:
The project's `.clang-format` file can take care of all of this for you.  
Use it only for new code. Old code is still using the old formatting at the moment.  

#### One line, one idea
##### Line size
You have a screen that can contain more than 150 or 160 characters easily with huge characters. Don't restrict it to 80.
##### Line breaks
Keep the code into one line where possible. Unless you are expressing more than one idea.
```c
// Good: 2ideas, 2lines
if (cond) { doThing(); }
else { doOtherThing(); }

// Bad: 2 ideas, 8 lines
if (cond)
{
  doThing();
}
else
{
  doOtherThing();
}
```
#### Tab size
Tab formatting is not reliable across IDEs. Use spaces. 
Indent with 2 spaces for all new code in the project.
Old code uses tabs, but will eventually be changed if possible.

#### Everything else:
Use the `.clang-format` file.



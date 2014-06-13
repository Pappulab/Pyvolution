Pyvolution
==========
Qualitative description of rules:
Living costs energy; make sure that your animal has enough sugar to support all of the calorie requirements of its actions.  Move around to find areas with enough food to eat so that it at least supports your energy needs.  Store extra energy as fat so that when you run out of food to eat you have reserves to move somewhere new.  Sugars are unstable and will disappear very quickly.  Spend energy to grow to be a full sized animal, you will be able to reach more food from where ever you are standing, however, this energy can never be reduced back to sugars.  Being larger is more expensive than being smaller, but not by much.  It is cheaper to have one animal than two animals of half the size.  It is expensive to accelerate very quickly.  Turning becomes more expensive if you are moving fast and making sharp turns, slow down if you need to turn sharply.  Once you have surplus reserves and are fully grown, spend energy to have a child.  

Required Orders:
Orders.AccForward: How much should your animals speed change by in the next time step?  Negative numbers reduce your speed.
Orders.Turn: How far should your animal turn in degrees (360 is full circle).  Positive numbers turn right, negative numbers turn left.
Orders.Eat: Should your animal eat the food in front of it?  Setting to 1 will make your animal eat, 0 will make it stand still.
Orders.Grow: How many calories should be spent growing your animal.  
Orders.Store: How many calories should be stored as fat.  A negative number will metabolize your fat back into sugars
Orders.Reproduce: How calories should be spent growing an unborn child.  Zero will indicate you are not growing a child any larger this step and negative 1 will give birth.
Memory: What memory should be stored for future use
Training: What training should be stored for future use

Important variables for your animal:
Animal.X(0): X position of your animal
Animal.X(1): Y position of your animal
Animal.V : Velocity of your animal
Animal.Sugar : Energy that can be spent by your animal
Animal.Fat : Long term energy storage
Animal.Size : Size of your animal
Animal.Stomach : Amount of vegetation in your stomach
Animal.Unborn : Size of child you are growing
Animal.Memory : Memory of your animal (lost every generation)
Animal.Training : Training of your animal (passed on every generation)






Quantitative Rules
Eating:
Min(Localfood/10,sqrt(size)/5) :  You can eat 10% of the food in reach, up to a fraction of your size. (you have a limited mouth)

Types of Energy:
Size: Total mass of your animal 
Sugars: Total energy available in muscles (short term use)
Stomach: Total calories worth of food that is being digested

Costs of Living:
√(Size+fat)/√1000 : As you get larger, storing energy becomes more efficient
.01*Calories: A fraction of your short term energy is lost
Stomach is free.

Costs of Moving:
√(Size+fat)/√1000 *Velocity
√(Size+fat)/√1000 *4*Acceleration^2 (slowing down is free)
√(Size+fat)/√1000 /202*Velocity*Turning^2
   Slower Accelerating and turning are more efficient 

Food Metabolism:
Stomach/200 : Every step, half a percent of your stomach gets processed
Half of your processed food is converted into sugars.

Growing:
Every calorie spent increases your size by 1. 
Every calorie spent increases your fat by 1.
Every 2 units of fat spent gives you 1 sugar in return.  Fat shouldn’t be used as short term storage.

Reproducing:
Offspring have a size and fat of 20% of the size spent to produce them
Offspring have sugar and stomach of 10% of the size spent to produce them
Unborn children cost √Unborn/√1000

Memory/Training:
Memory stores a class for your memory from the previous step.  Assign more memory by changing the getmemory function at the end of the animal file to a longer list of zeros.
Memory[0]=LocalFood stores the current local food to be used in analysis in a future time step.  

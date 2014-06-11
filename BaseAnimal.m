function [Orders,M] = BaseAnimal(A,LocalFood)

Orders.AccForward=0;
Orders.Turn=0;
Orders.Eat=1;
Orders.Reproduce=0;
Orders.Grow=0;

GoalCalories=10;
GoalSize=100;
GoalFood=20*(A.Size^.5/10000+A.Calories/500);

%says if the animal has any memory
if ~isfield(A,'M') 
M.LocalFood=LocalFood;
end
%determines if the animal should grow
if A.Calories>GoalCalories 
    Orders.Grow=(A.Calories-GoalCalories)/10;
elseif A.Calories<GoalCalories/2
    Orders.Grow=A.Calories-GoalCalories/2;
end
%determine if the animal should reproduce
% if A.Size>2*GoalSize
%     Orders.Reproduce=GoalSize/2;
% end
%determine if the animal should move:
if LocalFood<GoalFood && A.V==0
    Orders.AccForward=1;
end
% should stop
if LocalFood>GoalFood && A.V~=0
    Orders.AccForward=-1;
end
% should turn
if LocalFood<GoalFood && A.V~=0
    Orders.Turn=15;
end

% Store Stuff in Memory:
M.LocalFood=LocalFood;

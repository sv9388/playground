
clear;
printf('Loading boatloads of data. This will of course take time in your antique machine\n');
load('sample.mat');
%X = [1 2 3;4 5 6];
%y = [7;8];
X
y
printf('Aaaannnd done\n');
k = 21;
m = size(X,1);
n = size(X,2);
printf('Boo! Loaded. Continue');
pause;

%%Basic Checks & Playground
rand_indices = randperm(m);
X1 = X!=0;
%sel = X1(rand_indices(1:100),:);
%displayData(sel);

%%test data
testX = load('test_sample.txt');
testX1 = testX!=0;
%sel = testX1;
test_count = size(testX,1);
pred = zeros(test_count,1);

%% Hamming Distance
printf('Calculating Hamming Distance')
for test=1:test_count
	dist = zeros(m,1);
	for i=1:m
		dist(test)=sum(xor(X1(i,:),testX1(test,:)));
        end;
	indices = find(dist==max(dist));
	pred(test) = mode(y([indices],1));
end;
pred

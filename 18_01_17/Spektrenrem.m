clear all
close all
%spectrumnumbers to import
%UntergrundRem = 1:100;
UntergrundRem = [17 19 56 65 75 76]; %specificdata to import
for i=1:length(UntergrundRem)
    
    figure % creates a new figure
dateiC = sprintf('Ausheiz2Flake%d_1.txt',UntergrundRem(i)); % dateiC = string; %d is replaced with the value of UntgergrundRem(i)
C = importdata(dateiC); % import the data
xC = C(:,1)';
yC = C(:,2)';
%%yC1 = yC-min(yC);
plot(xC,yC,'b')
hold on
%remove the spikes
for k = 1:(length(yC)-1)
    if ((yC(k)/yC(k+1))<0.9)
        yC(k+1) = yC(k);
    else
        yC(k+1) = yC(k+1);
    end
end

%yC = yC-min(yC);
plot(xC,yC,'g')
%figure configuration
title(sprintf('Emitter %d',UntergrundRem(i)))
xlabel('Wavelength \lambda [nm]')
ylabel('Intensity [a.u.]')
end
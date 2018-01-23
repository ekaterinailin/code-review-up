clear all 
close all
l = [52 65 75 76 95]; %76 85 88 93 95 96 97];
c = 3e8;
h = 6.626e-34;
e = 1.602e-19;
for i = 1:length(l)        
    datei = sprintf('SpektrumFlake%d_600_800.txt',l(i));
    data = importdata(datei);
    x = data(:,1)';
    x2 = h*c./x/e/1e-9;
    x2min = min(x2);
    x2max = max(x2);
    y = data(:,2)';
    ymax = max(y);
    x2 = x2-x2(find(y==ymax));
    y = (y-min(y))/(max(y-min(y)));
    plot(x2,y,'LineWidth',0.1)
    hold on
    axis([-0.4 0.05 0 1])
    xlabel('\DeltaE (eV)')
    ylabel('Intensität')
    %% find deltaE between zpl & sideband
    startvalue = -0.14;
    endvalue = -0.18;
    stepwidth = 2.0013e-5;
    xstart = max(find(x2+stepwidth>startvalue));
    xend = min(find(x2-stepwidth<endvalue));
    max1 = y(xstart);
    for m = xstart:xend-1
        if (max1-y(m+1))>0
           max1 = max1;
        else
            max1 = y(m+1);
        end
    end
        posmax1y = find(y == max1);
        a = length(posmax1y);
       while (a ~= 1)
            if (posmax1y(a)-xend>0 || xstart-posmax1y(a)>0)
                posmax1y(a) = [];
                a = a-1;
            else
                posmax1y = posmax1y(a);
                a = 1;
            end
        end
        posmax(i) = x2(posmax1y);

end
posmax(posmax==0)=[];
meean = mean(posmax);
meanerror = std(posmax)/sqrt(length(posmax));
str = {'\DeltaE(ZPL-1.SB) = 162,1 \pm 2,2 meV'};
text(-0.38,0.7,str,'fontsize',14)
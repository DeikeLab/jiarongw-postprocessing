clear 
close all
warning off;
clc

% Size of the plot is twice the real size
% fontsize should be 2*12;
OneC = [5 10 19 19]; % in picas 
TwoC = [5 10 39 39]; % in picas
Cust = [5 10 19 28]; % in picas
OneC = OneC * 12; % in points
TwoC = TwoC * 12; % in points
Cust = Cust * 12; % in points
FONTSIZE       = 10; %in  points
FONTSIZE_LATEX = 10*1.5; %in  points
TICKLENGTH = [0.015 0.0075];
LINEWIDTH = 1;
MARGIN = 1;
MARKERSIZE = 5;
% ###################################################
% Comment these lines went saving in pdf
% FONTSIZE = FONTSIZE/1.5;
% FONTSIZE_LATEX = FONTSIZE_LATEX/1.5;
% ###################################################
% figure;
% set(gcf,'Units','points');
% set(gcf,'Position',TwoC);
% set(gcf,'color','w');
% GCF = get(gcf,'Position'); % in pixels
% % GCF = GCF / 96; % in inches
% set(gcf,'PaperUnits','points')
% set(gcf,'PaperSize',[GCF(3) GCF(4)])
% set(gcf,'PaperPosition',[0 0 GCF(3) GCF(4)])


T1 = datenum(2013,11,11,08,00,00);
T2 = datenum(2013,11,15,21,00,00);
T3 = datenum(2013,11,19,07,30,00);
T4 = datenum(2013,11,20,03,00,00);

path_in = '';

load([path_in 'WC_SIO_30min_averages.mat'])
load([path_in 'ASIFLUX_WINDFRAME_W0_UWcorrected_nfft36000_RAW_with_TSC.mat'])
% 
% path_out = [pwd '\PLOTS\'];
% mkdir(path_out)

path_out = '.';

MAST.time = EC_MEAN_1.time;
MAST.Z = [EC_MEAN_1.z ; EC_MEAN_2.z ; EC_MEAN_3.z ; EC_MEAN_4.z ; EC_MEAN_5.z];
MAST.U = [EC_MEAN_1.Uabs ; EC_MEAN_2.Uabs ; EC_MEAN_3.Uabs ; EC_MEAN_4.Uabs ; EC_MEAN_5.Uabs];

%% DISCARD MAST DATA in the wake of FLIP or the MAST.
MAST.PSI = nanmean([EC_MEAN_1.psi_Vnull ; EC_MEAN_2.psi_Vnull ; EC_MEAN_3.psi_Vnull ; EC_MEAN_4.psi_Vnull ; EC_MEAN_5.psi_Vnull],1);
I = find(MAST.PSI > -45 & MAST.PSI < 135);
Ibad = setdiff(1:length(MAST.time),I);
MAST.U(:,Ibad) = nan;

z = 4:1:15;
for i = 1:length(MAST.time)
    
    try
        MAST.U10(1,i) = interp1(MAST.Z(:,i),MAST.U(:,i),10,'linear');
        MAST.Uzr(:,i) = interp1(MAST.Z(:,i),MAST.U(:,i),z,'linear');
    catch
        MAST.U10(1,i) = nan;
        MAST.Uzr(:,i) = nan(length(z),1);
    end
end

%%
WC = WC_SIO;
WC.R = WC.NB_num ./ WC.Nt;
for i = 1:length(WC.time)
    I = find(WC.R(:,i) < 0.9,1,'first');
    J = find(WC.CNR(:,i) < -22,1,'first');
    K = min([I,J]);
    WC.Uh(K:end,i) = nan;
end

%% create continuous record with nan when no data
T = min(WC.time):1/48:max(WC.time);
[~,I,J] = intersect(round(T*48)/48,round(WC.time*48)/48);
field = fieldnames(WC);
clear wc
wc.time = repmat(T,20,1);
for k = 2:length(field)
    name = char(field(k,:));
    eval(['wc.' name ' = nan(size(WC.' name ',1),length(T));'])
    eval(['wc.' name '(:,I) = WC.' name '(:,J);'])
end

[~,I,J] = intersect(round(T*48)/48,round(MAST.time*48)/48);
field = fieldnames(MAST);
clear mast
mast.time = repmat(T,5,1);
for k = 2:length(field)
    name = char(field(k,:));
    eval(['mast.' name ' = nan(size(MAST.' name ',1),length(T));'])
    eval(['mast.' name '(:,I) = MAST.' name '(:,J);'])
end

%%
close all

% 1 point = 1.333 pixels.
% 1 pica = 16 px = 12 points.
% 1 inch = 96 px = 72 points = 6 picas.
% The max width seems to be 6.5 inch = 39 picas = 624 pixels (2 columns).
% The max heigth seems to be 8 inch = 48 picas = 768 pixels (but depends on the caption).
OneC = [5 10 19 19]; % in picas 
TwoC = [5 10 39 48]; % in picas 
CUST = [5 10 39 28]; % in picas
OneC = OneC * 12; % in points
TwoC = TwoC * 12; % in points
CUST = CUST * 12; % in points
FONTSIZE       = 10; %in  points
FONTSIZE_LATEX = 12; %in  points
TICKLENGTH=[0.0075 0.003];
LINEWIDTH = 1;

Xleft  = 734298.4;
Xright = 734310.85;
Xind=2; Yind=4;
POS1  = [0.08 0.55 0.8 0.43];
POS2  = [0.08 0.10 0.8 0.43];


figure;
set(gcf,'Units','points');
set(gcf,'Position',CUST);
set(gcf,'color','w');
GCF = get(gcf,'Position'); % in pixels
% GCF = GCF / 96; % in inches
set(gcf,'PaperUnits','points')
set(gcf,'PaperSize',[GCF(3) GCF(4)])
set(gcf,'PaperPosition',[0 0 GCF(3) GCF(4)])

XLa = -POS1(1)/POS1(3) + 0.01;
XRa = 1 + (1 -POS1(1)-POS1(3))/POS1(3) - 0.01;

XLIM = [datenum(2013,11,11,00,00,00) datenum(2013,11,22,12,00,00)];
YLIM = [1 500];
DT = 8; % in hours
T = unique(floor([XLIM(1):1/24*DT:XLIM(2)]*24)/24);

XTICK1 = unique(floor(T));

XTICK2 = T;
XTICKLABEL2 = datestr(XTICK2,'dd');
for i = 1:length(T)
    if T(i) ~= floor(T(i))
        XTICKLABEL2(i,:) = '  ';
    end
end

XTICK3 = unique(floor(T*2)/2);
XTICKLABEL3 = datestr(XTICK3,'dd');
for i = 1:length(XTICK3)
    if mod(i,2) == 1
        XTICKLABEL3(i,:) = '  ';
    end
end

S1 = subplot('position',POS1);
    hold on; grid on;
    [~,h1] = contourf(wc.time,wc.Z,wc.Uh);
    set(h1,'LevelList',[0:0.1:15])
    set(h1,'LineStyle','none')
    [~,h2] = contourf(mast.time,mast.Z,mast.U);
    set(h2,'LevelList',[0:0.5:15])
    set(h2,'LineStyle','none')
    set(gca,'Yscale','log')
    set(gca,'fontsize',FONTSIZE,'Ycolor','k');
    xlim(XLIM)
    ylim(YLIM)
    set(gca,'Xtick',[])
    set(gca,'Ytick',[])
    set(gca,'XtickLabel',[])
    set(gca,'YtickLabel',[])
    
    C1 = colorbar;
    set(gca,'position',POS1);
    caxis([0 13])
    set(get(C1,'Ylabel'),'String','U (m/s)')
    POSC1 = get(C1,'Position');
    set(C1,'Position',[POSC1(1:2) POSC1(3)/2 POSC1(4)])
    
    set(gca,'color','none');
    ax = copyobj(gca,gcf);
    ay = copyobj(gca,gcf);
    abox = copyobj(gca,gcf);
    set(gca,'visible','off');
    set(gca,'position',POS1,'color','none');
    set(abox,'position',POS1,'color','none');
    set(ax,'position',POS1,'color','none');
    set(ay,'position',POS1,'color','none');
    delete(findobj(gca,'Type','surface'))
    delete(findobj(ax,'Type','surface'))
    delete(findobj(ay,'Type','surface'))

    set(ax,'color','none','xtick',XTICK1,'tickdir','in','box','off','Xcolor','k')
    set(ax,'YaxisLocation','Right','YtickLabel',[])
    set(ax,'linewidth',0.5)
    set(ax,'Xgrid','on','Ygrid','on')

    set(ay,'color','none','xtick',[],'tickdir','out','box','off','Ycolor','k','Ytick',[1 10 100 300],'YtickLabel',[1 10 100 300])
    Y1 = get(ay,'Ylabel');
    set(Y1,'String','$z \ \mathrm{(m)}$','fontsize',FONTSIZE_LATEX,'interpreter','latex');
    set(Y1,'HorizontalAlignment','center','VerticalAlignment','top');
    set(Y1,'Units','Normalized','Position',[XLa 0.5 0]);

    set(abox,'color','none','xtick',[],'ytick',[],'box','on','Linewidth',1,'Xtick',XTICK1)

    Te=text(0,0,'(a)');
    set(Te,'HorizontalAlignment','Left','VerticalAlignment','bottom','fontsize',FONTSIZE)
    set(Te,'Units','normalized','Position',[0.02 0.02]);
    set(Te,'BackgroundColor','w','Margin',0.1);

  
S2 = subplot('position',POS2);
    coul = jet(length(T));
    hold on; grid on
    for i = 1:length(T)
        Im = find( round(mast.time(1,:)*48) == round(T(i)*48));
        Iw = find( round(wc.time(1,:)*48)   == round(T(i)*48));
        if isempty(Im) | isempty(Iw)
            continue
        end
        Umin = min(cat(1,mast.U(:,Im),wc.Uh(:,Iw)));
        Umax = max(cat(1,mast.U(:,Im),wc.Uh(:,Iw)));
        
        temp = (wc.Uh(:,Iw)-Umin) ./ (Umax-Umin);
        temp = temp * DT / 24;
        temp = temp + T(i);
%         plot(temp,wc.Z(:,Iw),'color',coul(i,:),'Linewidth',1.5);
        plot(temp,wc.Z(:,Iw),'b','Linewidth',1);
    
        temp = (mast.U(:,Im)-Umin) ./ (Umax-Umin);
        temp = temp * DT / 24;
        temp = temp + T(i);
%         plot(temp,mast.Z(:,Im),'color',coul(i,:),'Linewidth',1.5);
        plot(temp,mast.Z(:,Im),'b','Linewidth',1);
        
%         plot(T(i),1,'o','color',coul(i,:),'MarkerFaceColor',coul(i,:),'MarkerSize',2)
    end
    set(gca,'Yscale','log')
    set(gca,'Fontsize',FONTSIZE)
    xlim(XLIM)
    ylim(YLIM)
%     set(gca,'Xtick',XTICK2)
%     set(gca,'Ytick',[1 10 100 300])
    set(gca,'XtickLabel',[])
    set(gca,'YtickLabel',[])
    
%     C2 = colorbar;
%     set(gca,'position',POS2);
%     colormap(S2,jet(length(T)))
%     caxis([min(T) max(T)])
%     set(C2,'YTick',unique(floor(T)))
%     set(C2,'YTickLabel',datestr(get(C2,'YTick'),'dd'))
%     set(get(C2,'Ylabel'),'String','Days of November 2013')
%     POSC2 = get(C2,'Position');
%     set(C2,'Position',[POSC2(1:2) POSC2(3)/2 POSC2(4)])
    
    % ADD reference for Us
    Tr0 = datenum(2013,11,21,08,00,00);
    Tr1 = Tr0 + DT/24;
    Y = 1.5;
    plot([Tr0 Tr1],[Y Y],'k','Linewidth',1.5)
    T0 = text(Tr0,Y-0.05,'0','Fontsize',7,'HorizontalAlignment','center','VerticalAlignment','Top');
    T1 = text(Tr1,Y-0.05,'1','Fontsize',7,'HorizontalAlignment','center','VerticalAlignment','Top');
    T2 = text((Tr0+Tr1)/2,Y+0.05,'U_s','Fontsize',7,'HorizontalAlignment','center','VerticalAlignment','Bottom');
    
    set(gca,'color','none');
    ax = copyobj(gca,gcf);
    axx = copyobj(gca,gcf);
    ay = copyobj(gca,gcf);
    abox = copyobj(gca,gcf);
    set(gca,'visible','off');
    set(gca,'position',POS2,'color','none');
    set(abox,'position',POS2,'color','none');
    set(ax,'position',POS2,'color','none');
    set(axx,'position',POS2,'color','none');
    set(ay,'position',POS2,'color','none');
    delete(findobj(gca,'Type','surface'))
    delete(findobj(ax,'Type','surface'))
    delete(findobj(axx,'Type','surface'))
    delete(findobj(ay,'Type','surface'))

    set(ax,'color','none','xtick',XTICK2,'tickdir','in','box','off','Xcolor','k')
    set(ax,'YaxisLocation','Right','YtickLabel',[])
    set(ax,'linewidth',0.5)
    set(ax,'Xgrid','on','Ygrid','off')

    set(ay,'color','none','xtick',[],'tickdir','out','box','off','Ycolor','k','Ytick',[1 10 100 300],'YtickLabel',[1 10 100 300])
    Y1 = get(ay,'Ylabel');
    set(Y1,'String','$z \ \mathrm{(m)}$','fontsize',FONTSIZE_LATEX,'interpreter','latex');
    set(Y1,'HorizontalAlignment','center','VerticalAlignment','top');
    set(Y1,'Units','Normalized','Position',[XLa 0.5 0]);
    set(ay,'Xgrid','off','Ygrid','on')

    set(abox,'color','none','xtick',[],'ytick',[],'box','on','XTick',XTICK1,'LineWidth',1)
    
    set(ax,'color','none','xtick',XTICK3,'xtickLabel',XTICKLABEL3,'tickdir','out','box','off','Xcolor','k')
    set(ax,'YaxisLocation','Right','Ytick',[])
    set(ax,'linewidth',0.5)
    set(ax,'Xgrid','off','Ygrid','off')

    Te=text(0,0,'(b)');
    set(Te,'HorizontalAlignment','Left','VerticalAlignment','bottom','fontsize',FONTSIZE)
    set(Te,'Units','normalized','Position',[0.02 0.02]);
    set(Te,'BackgroundColor','w','Margin',0.1);
    
    X2 = get(ax,'Xlabel');
    set(X2,'String','Days of November 2013','fontsize',FONTSIZE);
    set(X2,'units','Normalized');
    set(X2,'HorizontalAlignment','center','VerticalAlignment','top')
    set(X2,'Position',[0.5 -0.125 0]);
% 
print -painters -dpdf Figure04.pdf          % save lines, points, text, labels, etc ...
% print -painters -dpng Figure04.png          % save lines, points, text, labels, etc ...
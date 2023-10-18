for i = 1:length(T)
    Im = find( round(mast.time(1,:)*48) == round(T(i)*48));
    Iw = find( round(wc.time(1,:)*48)   == round(T(i)*48));
    if isempty(Im) | isempty(Iw)
        continue
    end
    U1 = wc.Uh(:,Iw);
    U2 = mast.U(:,Im);
    U2 = flip(U2);
    z1 = wc.Z(:,Iw);
    z2 = mast.Z(:,Im);
    z2 = flip(z2);
    U = cat(1, U2, U1);
    z = cat(1, z2, z1);
    formatSpec = './umean_%d.txt';
    filename = sprintf(formatSpec,i);
    head = {'z','U'};
    fid = fopen(filename,'w');
    fprintf(fid,'%s %s\n',head{:});
    fprintf(fid,'%d %d\n',[z U]');

    % myTable = struct2table(spec);
    % writetable(myTable,filename,'delimiter',',','append');
end
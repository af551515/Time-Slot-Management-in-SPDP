***********************************Sets*****************************************
set i 'nodes' /parking,d1*d4,r1*r10/
    k 'vehicles' /k1*k10/
    g 'gooods'/g1*g10/
    p 'parking lots'/p1*p4/
    m 'time slots' /m1*m10/
;

* Driver is a truck in a 3PL company and
* rider is supplier


alias(i,j,r,d);

parameter parking(i);
parking(i)=0; parking('parking')=1;
parameter driver(i);
driver(i)=0; driver(i)$(ord(i)>1 and ord(i)<=5)=1;
parameter rider(i);
rider(i)=0; rider(i)$(ord(i)>5 and ord(i)<=card(i))=1;

parameter N1(i);
N1(i)=0;  N1(i)$(driver(i) or rider(i))=1;
parameter N2(i);
N2(i)=0;  N2(i)$(rider(i) or parking(i))=1;
***********************************Parameters***********************************
parameter fv(k) 'fixed cost of using truck'/
k1        100
k2        100
k3        175
k4        200
k5        100
k6        100
k7        175
k8        200
k9        200
k10       200
/;

table tt(i,j)
           parking     d1        d2        d3        d4        r1        r2        r3        r4        r5          r6        r7         r8        r9        r10
parking    0           40        60        60        40        63        57        72        63        45          63        45         57        63        85
d1         40          0         72        100       57        28        40        60        63        45          85        82         89        102       117
d2         60          72        0         85        100       72        108       40        122       28          20        89         45        72        134
d3         60          100       85        0         72        122       108       117       100       89          72        28         45        20        60
d4         40          57        100       72        0         85        40        108       28        82          102       45         89        85        63
r1         63          28        72        122       85        0         63        45        89        45          89        108        102       120       144
r2         57          40        108       108       40        63        0         100       28        82          117       82         113       117       102
r3         72          60        40        117       108       45        100       0         122       28          60        113        82        108       156
r4         63          63        122       100       28        89        28        122       0         100         126       72         117       113       80
r5         45          45        28        89        82        45        82        28        100       0           45        85         60        82        128
r6         63          85        20        72        102       89        117       60        126       45          0         82         28        57        126
r7         45          82        89        28        45        108       82        113       72        85          82        0          60        45        45
r8         57          89        45        45        89        102       113       82        117       60          28        60         0         28        102
r9         63          102       72        20        85        120       117       108       113       82          57        45         28        0         80
r10        85          117       134       60        63        144       102       156       80        128         126       45         102       80        0

parameter ct '$20 per hour equivalent to $0.33 per minute';
ct= 0.67;

parameter co ;
co= 0.33;

parameter cap(k)/
k1        300
k2        300
k3        400
k4        400
k5        300
k6        300
k7        400
k8        400
k9        400
k10       400
/;
cap(k)=cap(k)-200;
parameter ept(r)/
r1        60
r2        60
r3        120
r4        180
r5        60
r6        60
r7        120
r8        180
r9        60
r10       60
/;
parameter lpt(r) 'late'/
r1        120
r2        180
r3        180
r4        240
r5        120
r6        180
r7        180
r8        240
r9        240
r10       240
/;
lpt(r)=lpt(r)-60;
ept(r)=ept(r)-60;
parameter ltu(k)/
k1 = 480
k2 = 420
k3 = 420
k4 = 360
k5 = 480
k6 = 420
k7 = 420
k8 = 360
k9 = 360
k10 =360
/;

parameter dtu;
dtu= 240;

parameter st(i);
st(i)= 30;

parameter bigm;
bigm=10000;


table  s(r,g) 'production by supplier r fpr goods g'
          g1       g2       g3       g4       g5       g6       g7       g8       g9       g10
r1        0        10       4        10       0        10       4        10       10       10
r2        5        10       2        10       5        10       2        10       10       10
r3        10       0        3        0        10       0        3        0        0        0
r4        5        0        0        0        5        0        0        0        0        0
r5        0        10       4        10       0        10       4        10       10       10
r6        5        10       2        10       5        10       2        10       10       10
r7        10       0        3        0        10       0        3        0        0        0
r8        5        0        5        0        5        0        5        5        5        5
r9        5        0        5        5        5        0        5        5        5        5
r10       5        0        5        5        5        0        5        5        5        5
;

parameter dem(g)'demand for each goods'/
g1 = 30
g2 = 30
g3 = 20
g4 = 40
g5 = 30
g6 = 30
g7 = 20
g8 = 40
g9 = 40
g10= 40
/;

parameter v(g) 'volume of each goods'/
g1 = 3
g2 = 4
g3 = 6
g4 = 3
g5 = 3
g6 = 3
g7 = 4
g8 = 3
g9 = 4
g10= 4
/;

parameter ns(k)'the Number of required time slots for unloading in parking'/
k1        2
k2        3
k3        3
k4        4
k5        2
k6        3
k7        3
k8        4
k9        4
k10       4
/;

parameter ep 'small number';
ep=0.1;

parameter n 'upperbound for m as time slots';
n=10;

parameter minn 'upperbound for m as time slots';
minn=60;
**********************************Variables*************************************
binary variables x(i,j,k),y(i,k),w(p,m,k);
positive variable t(i,k),alpha1(k),alpha2(k),alpha1a(k),alpha2a(k),alpha1(k),alpha2(k),o(r,g,k);
binary variable psi(p,m,k), b(m,k);
integer variable ell, you;
free variables z1;
****Preprocessing********
x.fx(i,'parking',k)$driver(i)=0;
**********************************Equations*************************************
equations
obj1
obj2
eq2(r)
eq3(i)
eq4(r,k)
eq5(j,k)
eq6(g)
eq7(k)
eq8(r,g,k)
eq9(i,j,k)
eq10_1(r,k)
eq10_2(r,k)
eq11(k)
eq13(m,k)
eq14(p,m)
eq15(p,k,m)
eq19(k),eq20(k),eq21(k),eq22(k),eq23(k),eq24(k),eq25(k)
eq28(k),eq29(k),eq30(k),eq31(k)
eq35(k),eq36(p,k,m),eq37(p,k,m),eq38(p,k,m)
eq40(m,k),eq41(m,k)
eq191(k)
vi1,vi2,vi3,vi4
;


obj1..                                                                           z1=e=sum((k),fv(k)*y('parking',k))+sum((k,i,j), ct*tt(i,j)*x(i,j,k))+co*sum(k,(alpha1a(k)+alpha2a(k)));
obj2..                                                                           z1=e=sum((k),fv(k)*y('parking',k))+sum((k,i,j), ct*tt(i,j)*x(i,j,k))+co*sum(k,(alpha1(k)+alpha2(k)));
eq2(j)$rider(j)..                                                                sum((i,k)$(n1(i) and (ord (i)<> ord(j))),x(i,j,k))=l=1;
eq3(i)$rider(i)..                                                                sum((j,k)$(n2(j) and (ord (i)<> ord(j))),x(i,j,k))=l=1;
eq4(r,k)$rider(r)..                                                              sum(i$(n1(i) and (ord (i)<> ord(r))),x(i,r,k))=e=
                                                                                 sum((j)$(n2(j) and (ord (j)<> ord(r))),x(r,j,k));

eq5(j,k)$n2(j)..                                                                 sum(i$(n1(i) and (ord (i)<> ord(j))),x(i,j,k))=e=y(j,k);
eq6(g)..                                                                         sum((r,k)$(rider(r)),o(r,g,k))=g=dem(g);
eq7(k)..                                                                         sum((r,g)$(rider(r)),o(r,g,k)*v(g))=l=cap(k);
eq8(r,g,k)$rider(r)..                                                            o(r,g,k)=l= y(r,k)* s(r,g);
eq9(i,j,k)$(n1(i)and n2(j))..                                                    t(i,k)+st(i)+tt(i,j)-bigm*(1-x(i,j,k))=l=t(j,k);
eq10_1(r,k)$rider(r)..                                                           t(r,k)=l=y(r,k)*lpt(r);
eq10_2(r,k)$rider(r)..                                                           y(r,k)*ept(r)=l=t(r,k);
eq11(k)..                                                                        t('parking',k)=l=ltu(k)*y('parking',k);

eq13(m,k)..                                                                      sum(p,w(p,m,k))=l=y('parking',k);
eq14(p,m)..                                                                      sum(k,w(p,m,k))=l=1;

eq15(p,k,m)..                                                                    w(p,m+1,k)=l=w(p,m,k)+bigm*(1-b(m,k));



eq19(k)..                                                                        alpha1(k)-alpha2(k)=e=dtu-t('parking',k);
eq191(k)..                                                                       alpha1(k)-alpha2(k)=e=dtu*y('parking',k)-t('parking',k);
eq20(k)..                                                                        alpha1a(k)=l=bigm*y('parking',k);
eq21(k)..                                                                        alpha1a(k)=l=alpha1(k);
eq22(k)..                                                                        alpha1a(k)=g=alpha1(k)-bigm*(1-y('parking',k));
eq23(k)..                                                                        alpha2a(k)=l=bigm*y('parking',k);
eq24(k)..                                                                        alpha2a(k)=l=alpha2(k);
eq25(k)..                                                                        alpha2a(k)=g=alpha2(k)-bigm*(1-y('parking',k));

eq28(k)..                                                                        ell(k)=l=(t('parking',k)/minn)+1;
eq29(k)..                                                                        ell(k)=g=(t('parking',k)/minn)+1-1+ep;
eq30(k)..                                                                        you(k)=l=(t('parking',k)/minn)+ns(k);
eq31(k)..                                                                        you(k)=g=(t('parking',k)/minn)+ns(k)-1+ep;

eq35(k)..                                                                        y('parking',k)*ns(k)=l=sum((p,m),psi(p,m,k));
eq36(p,k,m)..                                                                    psi(p,m,k)=l=w(p,m,k);
eq37(p,k,m)..                                                                    psi(p,m,k)=l=bigm*b(m,k);
eq38(p,k,m)..                                                                    psi(p,m,k)=g=w(p,m,k)-bigm*(1-b(m,k));

eq40(m,k)..                                                                      b(m,k)=l=1+((you(k)-ord(m))/n);
eq41(m,k)..                                                                      b(m,k)=l=1+((ord(m)-ell(k))/n);

vi1..sum(k,y('parking',k))=g=1;
vi2(k)..t('parking',k)=g=sum((i,j),tt(i,j)*x(i,j,k))+sum(i,st(i)*y(i,k));
vi3..sum((i,k)$(ord(i)=1),y(i,k))=g=6;
vi4(i,j)..sum(k,x(i,j,k)+x(j,i,k))=l=1

set iter/1*32/;
parameter results(iter,*);
$Ontext
model u0 /obj1,eq2,eq3,eq4,eq5,eq6,eq7,eq8,eq9,eq10_1,eq10_2,eq11,eq13,eq14,eq15,eq19,eq20,eq21,eq22,eq23,eq24,eq25,eq28,eq29,eq30,eq31,eq35,eq36,eq37,eq38,eq40,eq41/;
option optcr=0,optca=0, reslim=7200;
option limcol=10, limrow=100;
solve u0 minimizing z1 using rmip;
results('1','obj')=z1.l;
results('1','resusd')=u0.resusd;
results('1','nodusd')=u0.nodusd;
display x.l;
model u1 /obj1,eq2,eq3,eq4,eq5,eq6,eq7,eq8,eq9,eq10_1,eq10_2,eq11,eq13,eq14,eq15,eq19,eq20,eq21,eq22,eq23,eq24,eq25,eq28,eq29,eq30,eq31,eq35,eq36,eq37,eq38,eq40,eq41,vi1/;
option optcr=0,optca=0, reslim=7200;
option limcol=10, limrow=100;
solve u1 minimizing z1 using rmip;
results('2','obj')=z1.l;
results('2','resusd')=u1.resusd;
results('2','nodusd')=u1.nodusd;
model u2 /obj1,eq2,eq3,eq4,eq5,eq6,eq7,eq8,eq9,eq10_1,eq10_2,eq11,eq13,eq14,eq15,eq19,eq20,eq21,eq22,eq23,eq24,eq25,eq28,eq29,eq30,eq31,eq35,eq36,eq37,eq38,eq40,eq41,vi2/;
option optcr=0,optca=0, reslim=7200;
option limcol=10, limrow=100;
solve u2 minimizing z1 using rmip;
results('3','obj')=z1.l;
results('3','resusd')=u2.resusd;
results('3','nodusd')=u2.nodusd;
model u3 /obj1,eq2,eq3,eq4,eq5,eq6,eq7,eq8,eq9,eq10_1,eq10_2,eq11,eq13,eq14,eq15,eq19,eq20,eq21,eq22,eq23,eq24,eq25,eq28,eq29,eq30,eq31,eq35,eq36,eq37,eq38,eq40,eq41,vi3/;
option optcr=0,optca=0, reslim=7200;
option limcol=10, limrow=100;
solve u3 minimizing z1 using rmip;
results('4','obj')=z1.l;
results('4','resusd')=u3.resusd;
results('4','nodusd')=u3.nodusd;
model u4 /obj1,eq2,eq3,eq4,eq5,eq6,eq7,eq8,eq9,eq10_1,eq10_2,eq11,eq13,eq14,eq15,eq19,eq20,eq21,eq22,eq23,eq24,eq25,eq28,eq29,eq30,eq31,eq35,eq36,eq37,eq38,eq40,eq41,vi4/;
option optcr=0,optca=0, reslim=7200;
option limcol=10, limrow=100;
solve u4 minimizing z1 using rmip;
results('5','obj')=z1.l;
results('5','resusd')=u4.resusd;
results('5','nodusd')=u4.nodusd;
model un /obj2,eq2,eq3,eq4,eq5,eq6,eq7,eq8,eq9,eq10_1,eq10_2,eq11,eq13,eq14,eq15,eq191,eq28,eq29,eq30,eq31,eq35,eq36,eq37,eq38,eq40,eq41/;
option optcr=0,optca=0, reslim=7200;
option limcol=10, limrow=100;
solve un minimizing z1 using rmip;
results('6','obj')=z1.l;
results('6','resusd')=un.resusd;
results('6','nodusd')=un.nodusd;
model u7 /obj1,eq2,eq3,eq4,eq5,eq6,eq7,eq8,eq9,eq10_1,eq10_2,eq11,eq13,eq14,eq15,eq19,eq20,eq21,eq22,eq23,eq24,eq25,eq28,eq29,eq30,eq31,eq35,eq36,eq37,eq38,eq40,eq41,vi1,vi2/;
option optcr=0,optca=0, reslim=7200;
option limcol=10, limrow=100;
solve u7 minimizing z1 using rmip;
results('7','obj')=z1.l;
results('7','resusd')=u7.resusd;
results('7','nodusd')=u7.nodusd;
model u8 /obj1,eq2,eq3,eq4,eq5,eq6,eq7,eq8,eq9,eq10_1,eq10_2,eq11,eq13,eq14,eq15,eq19,eq20,eq21,eq22,eq23,eq24,eq25,eq28,eq29,eq30,eq31,eq35,eq36,eq37,eq38,eq40,eq41,vi1,vi3/;
option optcr=0,optca=0, reslim=7200;
option limcol=10, limrow=100;
solve u8 minimizing z1 using rmip;
results('8','obj')=z1.l;
results('8','resusd')=u8.resusd;
results('8','nodusd')=u8.nodusd;
model u9 /obj1,eq2,eq3,eq4,eq5,eq6,eq7,eq8,eq9,eq10_1,eq10_2,eq11,eq13,eq14,eq15,eq19,eq20,eq21,eq22,eq23,eq24,eq25,eq28,eq29,eq30,eq31,eq35,eq36,eq37,eq38,eq40,eq41,vi1,vi4/;
option optcr=0,optca=0, reslim=7200;
option limcol=10, limrow=100;
solve u9 minimizing z1 using rmip;
results('9','obj')=z1.l;
results('9','resusd')=u9.resusd;
results('9','nodusd')=u9.nodusd;
model un1 /obj2,eq2,eq3,eq4,eq5,eq6,eq7,eq8,eq9,eq10_1,eq10_2,eq11,eq13,eq14,eq15,eq191,eq28,eq29,eq30,eq31,eq35,eq36,eq37,eq38,eq40,eq41,vi1/;
option optcr=0,optca=0, reslim=7200;
option limcol=10, limrow=100;
solve un1 minimizing z1 using rmip;
results('10','obj')=z1.l;
results('10','resusd')=un1.resusd;
results('10','nodusd')=un1.nodusd;
model u11 /obj1,eq2,eq3,eq4,eq5,eq6,eq7,eq8,eq9,eq10_1,eq10_2,eq11,eq13,eq14,eq15,eq19,eq20,eq21,eq22,eq23,eq24,eq25,eq28,eq29,eq30,eq31,eq35,eq36,eq37,eq38,eq40,eq41,vi2,vi3/;
option optcr=0,optca=0, reslim=7200;
option limcol=10, limrow=100;
solve u11 minimizing z1 using rmip;
results('11','obj')=z1.l;
results('11','resusd')=u11.resusd;
results('11','nodusd')=u11.nodusd;
model u12 /obj1,eq2,eq3,eq4,eq5,eq6,eq7,eq8,eq9,eq10_1,eq10_2,eq11,eq13,eq14,eq15,eq19,eq20,eq21,eq22,eq23,eq24,eq25,eq28,eq29,eq30,eq31,eq35,eq36,eq37,eq38,eq40,eq41,vi2,vi4/;
option optcr=0,optca=0, reslim=7200;
option limcol=10, limrow=100;
solve u12 minimizing z1 using rmip;
results('12','obj')=z1.l;
results('12','resusd')=u12.resusd;
results('12','nodusd')=u12.nodusd;
model un2 /obj2,eq2,eq3,eq4,eq5,eq6,eq7,eq8,eq9,eq10_1,eq10_2,eq11,eq13,eq14,eq15,eq191,eq28,eq29,eq30,eq31,eq35,eq36,eq37,eq38,eq40,eq41,vi2/;
option optcr=0,optca=0, reslim=7200;
option limcol=10, limrow=100;
solve un2 minimizing z1 using rmip;
results('13','obj')=z1.l;
results('13','resusd')=un2.resusd;
results('13','nodusd')=un2.nodusd;
model u14 /obj1,eq2,eq3,eq4,eq5,eq6,eq7,eq8,eq9,eq10_1,eq10_2,eq11,eq13,eq14,eq15,eq19,eq20,eq21,eq22,eq23,eq24,eq25,eq28,eq29,eq30,eq31,eq35,eq36,eq37,eq38,eq40,eq41,vi3,vi4/;
option optcr=0,optca=0, reslim=7200;
option limcol=10, limrow=100;
solve u14 minimizing z1 using rmip;
results('14','obj')=z1.l;
results('14','resusd')=u14.resusd;
results('14','nodusd')=u14.nodusd;
model un3 /obj2,eq2,eq3,eq4,eq5,eq6,eq7,eq8,eq9,eq10_1,eq10_2,eq11,eq13,eq14,eq15,eq191,eq28,eq29,eq30,eq31,eq35,eq36,eq37,eq38,eq40,eq41,vi3/;
option optcr=0,optca=0, reslim=7200;
option limcol=10, limrow=100;
solve un3 minimizing z1 using rmip;
results('15','obj')=z1.l;
results('15','resusd')=un3.resusd;
results('15','nodusd')=un3.nodusd;
model un4 /obj2,eq2,eq3,eq4,eq5,eq6,eq7,eq8,eq9,eq10_1,eq10_2,eq11,eq13,eq14,eq15,eq191,eq28,eq29,eq30,eq31,eq35,eq36,eq37,eq38,eq40,eq41,vi4/;
option optcr=0,optca=0, reslim=7200;
option limcol=10, limrow=100;
solve un4 minimizing z1 using rmip;
results('16','obj')=z1.l;
results('16','resusd')=un4.resusd;
results('16','nodusd')=un4.nodusd;
model u17 /obj1,eq2,eq3,eq4,eq5,eq6,eq7,eq8,eq9,eq10_1,eq10_2,eq11,eq13,eq14,eq15,eq19,eq20,eq21,eq22,eq23,eq24,eq25,eq28,eq29,eq30,eq31,eq35,eq36,eq37,eq38,eq40,eq41,vi1,vi2,vi3/;
option optcr=0,optca=0, reslim=7200;
option limcol=10, limrow=100;
$Offtext
$Ontext
solve u17 minimizing z1 using rmip;
results('17','obj')=z1.l;
results('17','resusd')=u17.resusd;
results('17','nodusd')=u17.nodusd;
model u18 /obj1,eq2,eq3,eq4,eq5,eq6,eq7,eq8,eq9,eq10_1,eq10_2,eq11,eq13,eq14,eq15,eq19,eq20,eq21,eq22,eq23,eq24,eq25,eq28,eq29,eq30,eq31,eq35,eq36,eq37,eq38,eq40,eq41,vi1,vi2,vi4/;
option optcr=0,optca=0, reslim=7200;
option limcol=10, limrow=100;
solve u18 minimizing z1 using rmip;
results('18','obj')=z1.l;
results('18','resusd')=u18.resusd;
results('18','nodusd')=u18.nodusd;
model un5 /obj2,eq2,eq3,eq4,eq5,eq6,eq7,eq8,eq9,eq10_1,eq10_2,eq11,eq13,eq14,eq15,eq191,eq28,eq29,eq30,eq31,eq35,eq36,eq37,eq38,eq40,eq41,vi1,vi2/;
option optcr=0,optca=0, reslim=7200;
option limcol=10, limrow=100;
solve un5 minimizing z1 using rmip;
results('19','obj')=z1.l;
results('19','resusd')=un5.resusd;
results('19','nodusd')=un5.nodusd;
model u20 /obj1,eq2,eq3,eq4,eq5,eq6,eq7,eq8,eq9,eq10_1,eq10_2,eq11,eq13,eq14,eq15,eq19,eq20,eq21,eq22,eq23,eq24,eq25,eq28,eq29,eq30,eq31,eq35,eq36,eq37,eq38,eq40,eq41,vi1,vi3,vi4/;
option optcr=0,optca=0, reslim=7200;
option limcol=10, limrow=100;
solve u20 minimizing z1 using rmip;
results('20','obj')=z1.l;
results('20','resusd')=u20.resusd;
results('20','nodusd')=u20.nodusd;
model un6 /obj2,eq2,eq3,eq4,eq5,eq6,eq7,eq8,eq9,eq10_1,eq10_2,eq11,eq13,eq14,eq15,eq191,eq28,eq29,eq30,eq31,eq35,eq36,eq37,eq38,eq40,eq41,vi1,vi3/;
option optcr=0,optca=0, reslim=7200;
option limcol=10, limrow=100;
solve un6 minimizing z1 using rmip;
results('21','obj')=z1.l;
results('21','resusd')=un6.resusd;
results('21','nodusd')=un6.nodusd;
model un7 /obj2,eq2,eq3,eq4,eq5,eq6,eq7,eq8,eq9,eq10_1,eq10_2,eq11,eq13,eq14,eq15,eq191,eq28,eq29,eq30,eq31,eq35,eq36,eq37,eq38,eq40,eq41,vi1,vi4/;
option optcr=0,optca=0, reslim=7200;
option limcol=10, limrow=100;
solve un7 minimizing z1 using rmip;
results('22','obj')=z1.l;
results('22','resusd')=un7.resusd;
results('22','nodusd')=un7.nodusd;
model u23 /obj1,eq2,eq3,eq4,eq5,eq6,eq7,eq8,eq9,eq10_1,eq10_2,eq11,eq13,eq14,eq15,eq19,eq20,eq21,eq22,eq23,eq24,eq25,eq28,eq29,eq30,eq31,eq35,eq36,eq37,eq38,eq40,eq41,vi2,vi3,vi4/;
option optcr=0,optca=0, reslim=7200;
option limcol=10, limrow=100;
solve u23 minimizing z1 using rmip;
results('23','obj')=z1.l;
results('23','resusd')=u23.resusd;
results('23','nodusd')=u23.nodusd;
model un8 /obj2,eq2,eq3,eq4,eq5,eq6,eq7,eq8,eq9,eq10_1,eq10_2,eq11,eq13,eq14,eq15,eq191,eq28,eq29,eq30,eq31,eq35,eq36,eq37,eq38,eq40,eq41,vi2,vi3/;
option optcr=0,optca=0, reslim=7200;
option limcol=10, limrow=100;
solve un8 minimizing z1 using rmip;
results('24','obj')=z1.l;
results('24','resusd')=un8.resusd;
results('24','nodusd')=un8.nodusd;
model un9 /obj2,eq2,eq3,eq4,eq5,eq6,eq7,eq8,eq9,eq10_1,eq10_2,eq11,eq13,eq14,eq15,eq191,eq28,eq29,eq30,eq31,eq35,eq36,eq37,eq38,eq40,eq41,vi2,vi4/;
option optcr=0,optca=0, reslim=7200;
option limcol=10, limrow=100;
solve un9 minimizing z1 using rmip;
results('25','obj')=z1.l;
results('25','resusd')=un9.resusd;
results('25','nodusd')=un9.nodusd;
model un10 /obj2,eq2,eq3,eq4,eq5,eq6,eq7,eq8,eq9,eq10_1,eq10_2,eq11,eq13,eq14,eq15,eq191,eq28,eq29,eq30,eq31,eq35,eq36,eq37,eq38,eq40,eq41,vi3,vi4/;
option optcr=0,optca=0, reslim=7200;
option limcol=10, limrow=100;
solve un10 minimizing z1 using rmip;
results('26','obj')=z1.l;
results('26','resusd')=un10.resusd;
results('26','nodusd')=un10.nodusd;
model u27 /obj1,eq2,eq3,eq4,eq5,eq6,eq7,eq8,eq9,eq10_1,eq10_2,eq11,eq13,eq14,eq15,eq19,eq20,eq21,eq22,eq23,eq24,eq25,eq28,eq29,eq30,eq31,eq35,eq36,eq37,eq38,eq40,eq41,vi1,vi2,vi3,vi4/;
option optcr=0,optca=0, reslim=7200;
option limcol=10, limrow=100;
solve u27 minimizing z1 using rmip;
results('27','obj')=z1.l;
results('27','resusd')=u27.resusd;
results('27','nodusd')=u27.nodusd;
model un11 /obj2,eq2,eq3,eq4,eq5,eq6,eq7,eq8,eq9,eq10_1,eq10_2,eq11,eq13,eq14,eq15,eq191,eq28,eq29,eq30,eq31,eq35,eq36,eq37,eq38,eq40,eq41,vi1,vi2,vi3/;
option optcr=0,optca=0, reslim=7200;
option limcol=10, limrow=100;
solve un11 minimizing z1 using rmip;
results('28','obj')=z1.l;
results('28','resusd')=un11.resusd;
results('28','nodusd')=un11.nodusd;
model un12 /obj2,eq2,eq3,eq4,eq5,eq6,eq7,eq8,eq9,eq10_1,eq10_2,eq11,eq13,eq14,eq15,eq191,eq28,eq29,eq30,eq31,eq35,eq36,eq37,eq38,eq40,eq41,vi2,vi3,vi4/;
option optcr=0,optca=0, reslim=7200;
option limcol=10, limrow=100;
solve un12 minimizing z1 using rmip;
results('29','obj')=z1.l;
results('29','resusd')=un12.resusd;
results('29','nodusd')=un12.nodusd;
model un13 /obj2,eq2,eq3,eq4,eq5,eq6,eq7,eq8,eq9,eq10_1,eq10_2,eq11,eq13,eq14,eq15,eq191,eq28,eq29,eq30,eq31,eq35,eq36,eq37,eq38,eq40,eq41,vi1,vi2,vi4/;
option optcr=0,optca=0, reslim=7200;
option limcol=10, limrow=100;
solve un13 minimizing z1 using rmip;
results('30','obj')=z1.l;
results('30','resusd')=un13.resusd;
results('30','nodusd')=un13.nodusd;
model un14 /obj2,eq2,eq3,eq4,eq5,eq6,eq7,eq8,eq9,eq10_1,eq10_2,eq11,eq13,eq14,eq15,eq191,eq28,eq29,eq30,eq31,eq35,eq36,eq37,eq38,eq40,eq41,vi1,vi3,vi4/;
option optcr=0,optca=0, reslim=7200;
option limcol=10, limrow=100;
solve un14 minimizing z1 using rmip;
results('31','obj')=z1.l;
results('31','resusd')=un14.resusd;
results('31','nodusd')=un14.nodusd;
$Offtext
model un15 /obj2,eq2,eq3,eq4,eq5,eq6,eq7,eq8,eq9,eq10_1,eq10_2,eq11,eq13,eq14,eq15,eq191,eq28,eq29,eq30,eq31,eq35,eq36,eq37,eq38,eq40,eq41,vi1,vi2,vi3,vi4/;
option optcr=0,optca=0, reslim=7200;
option limcol=10, limrow=100;
solve un15 minimizing z1 using mip;
results('32','obj')=z1.l;
results('32','resusd')=un15.resusd;
results('32','nodusd')=un15.nodusd;

display results;
parameter f1,f2,f3,nv;
f1=sum((k),fv(k)*y.l('parking',k));
f2=sum((k,i,j), ct*tt(i,j)*x.l(i,j,k));
f3=co*sum(k,(alpha1.l(k)+alpha2.l(k)));
nv=sum((k),y.l('parking',k));
display w.l,f1,f2,f3,nv,t.l;

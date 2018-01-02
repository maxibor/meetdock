module mc11a90

  contains  

      subroutine mc11a(a,n,z,sig,w,ir,mk,eps)
      implicit real*8 (a-h,o-z)
      implicit integer*4 (i-n)
      dimension a(*),z(*),w(*)
      if(n.gt.1) goto 1
      a(1)=a(1)+sig *z(1)**2
      ir=1
      if(a(1).gt.0.)return
      a(1)=0.d0
      ir=0
      return
1     continue
      np=n+1
      if(sig.gt.0.d0) goto 40
      if(sig.eq.0.d0.or.ir.eq.0)return
      ti=1.d0/sig
      ij=1
      if(mk.eq.0) goto 10
      do 7 i=1,n
      if(a(ij).ne.0.d0)ti=ti+w(i)**2/a(ij)
7     ij=ij+np-i
      goto 20
10    continue
      do 11 i=1,n
11    w(i)=z(i)
      do 15 i=1,n
      ip=i+1
      v=w(i)
      if(a(ij).gt.0.) goto 12
      w(i)=0.d0
      ij=ij+np-i
      goto 15
12    continue
      ti=ti+v**2/a(ij)
      if(i.eq.n) goto 14
      do 13 j=ip,n
      ij=ij+1
13    w(j)=w(j)-v*a(ij)
14    ij=ij+1
15    continue
20    continue
      if(ir.le.0 ) goto 21
      if(ti.gt.0.) goto 22
      if(mk-1)40,40,23
21    ti=0.d0
      ir=-ir-1
      goto 23
22    ti=eps/sig
      if(eps.eq.0.)ir=ir-1
23    continue
      mm=1
      tim=ti
      do 30 i=1,n
      j=np-i
      ij=ij-i
      if(a(ij).ne.0.)tim=ti-w(j)**2/a(ij)
      w(j)=ti
30    ti=tim
      goto 41
40    continue
      mm=0
      tim=1.d0/sig
41    continue
      ij=1
      do 66 i=1,n
      ip=i+1
      v=z(i)
      if(a(ij).gt.0.) goto 53
      if(ir.gt.0 .or.sig.lt.0..or.v.eq.0.) goto 52
      ir=1-ir
      a(ij)=v**2/tim
      if(i.eq.n)return
      do 51 j=ip,n
      ij=ij+1
51    a(ij)=z(j)/v
      return
52    continue
      ti=tim
      ij=ij+np-i
      goto 66
53    continue
      al=v/a(ij)
      if(mm)54,54,55
54    ti=tim+v*al
      goto 56
55    ti=w(i)
56    continue
      r=ti/tim
      a(ij)=a(ij)*r
      if(r.eq.0.) goto 70
      if(i.eq.n) goto 70
      b=al/ti
      if(r.gt.4.) goto 62
      do 61 j=ip,n
      ij=ij+1
      z(j)=z(j)-v*a(ij)
61    a(ij)=a(ij)+b*z(j)
      goto 64
62    gm=tim/ti
      do 63 j=ip,n
      ij=ij+1
      y=a(ij)
      a(ij)=b*z(j)+y*gm
63    z(j)=z(j)-v*y
64    continue
      tim=ti
      ij=ij+1
66    continue
70    continue
      if(ir.lt.0)ir=-ir
      return
    end subroutine mc11a
!c-----------------------------------multiply vector z by inverse of factors in a
    subroutine  mc11e(a,n,z,w,ir)
      implicit real*8 (a-h,o-z)
      implicit integer*4 (i-n)
      dimension a(*),z(*),w(*)
      if(ir.lt.n)return
      w(1)=z(1)
      if(n.gt.1) goto 400
      z(1)=z(1)/a(1)
      return
400   continue
      do 402 i=2,n
      ij=i
      i1=i-1
      v=z(i)
      do 401 j=1,i1
      v=v-a(ij)*z(j)
401   ij=ij+n-j
      w(i)=v
402   z(i)=v
      z(n)=z(n)/a(ij)
      np=n+1
      do 411 nip=2,n
      i=np-nip
      ii=ij-nip
      v=z(i)/a(ii)
      ip=i+1
      ij=ii
      do 410 j=ip,n
      ii=ii+1
410   v=v-a(ii)*z(j)
411   z(i)=v
      return

    end subroutine mc11e

end module mc11a90

module mapping

  use run_parameter
  use particles
  use getmin
  use korobov
  use microb
!  use art_pro
  use proteins
  use energa

  implicit none

contains 

subroutine make_potential_map
!============================

  integer :: i, parti, Np2,npos
  integer :: sep,nsep, rot,nrot, gam
  integer :: sfirst,rfirst, nor, nmin
  integer :: posline

  real(8) ::  th1,ph1
  real(8) ::  ph2, th2, ps
  real(8) ::  xi,yi,zi
  real(8) ::  xj,yj,zj
  real(8) ::  x2,y2,z2
  real(8) ::  dx,dy,dz
  real(8) ::  Elj, Eelec, Etot
  real(8) ::  tmin, pmin, Psmin
  real(8) ::  amin, bmin, gmin 
  real(8) ::  Ermin,Erelec,Erlj

  real(8), dimension(6) :: grad
  real(8), dimension(N_vect_max) :: Emin, Emlj, Emelec

  character*1 :: chain, chain1, chain2
  character*3 :: snu,rnu
  character*50:: start_name

  logical :: restart_process

  restart_process=.false.
 
  Np2=prot_id(2)%Pstot_number
  do i=1,Nvect1 
    vecposition1(i)=i
  end do
  do i=1,Nvect2 
    vecposition2(i)=i
  end do
!  call kor_vect(nk1,vect_u1,Nvect1,phi1,theta1)
  call make_vect(vect_u1,Nvect1,phi1,theta1,vecposition1)
!  call kor_vect(nk2,vect_u2,Nvect2,phi2,theta2)
  call make_vect(vect_u2,Nvect2,phi2,theta2,vecposition2)

  allocate(score_pos(Nvect1*Nvect2*ngamma))

  Emin(:)=0.0
  Emlj(:)=0.0
  Emelec(:)=0.0

  evalf_number=0
  npos=0
  posline=0

  write(6,form_tens) 'Total number of positions around receptor', real(Nvect1)
  write(6,form_tens) 'Total number of positions around ligand', real(Nvect2)
  write(6,form_tens) 'Total number of gamma orientations', real(ngamma)
  write(6,*)

  call get_Psep(vect_u1)
  
  call check_starting_points
!  stop 'checking vectors'
 
  write(6,*) 'minimization loop'

  REWIND(94)

  inquire(file='temp_pos.dat',exist=restart_process)
  if(restart_process) then
    write(6,*) 'restart interrupted minimization'
    open(95,file='temp_pos.dat',status='old')
    read(95,*) npos
    close(95) 
    write(6,*) 'starting from position ',npos
  else
    write(6,*) 'no temp_pos found'
  end if

  do
    read(94,form_i,end=999) nsep,nrot,gam

    posline=posline+1 
    if(posline<npos) cycle

    npos=posline     

    open(95,file='temp_pos.dat')
    write(95,*) npos
    close(95)

    if(nsep<nsep1.or.nsep>nsep2) cycle
    if(nrot<nrot1.or.nrot>nrot2) cycle

!  do sep=1,Nvect1
!separation_loop :do nsep=nsep1,nsep2

    sep=vecposition1(nsep)

    nor=0
    nmin=1

!    do rot=1,Nvect2
!rotation_loop : do nrot=nrot1,nrot2  
      rot=vecposition2(nrot)
  
!      open(95,file='temp_global.dat')

      ph2=phi2(rot)
      th2=theta2(rot)

      write(snu,'(i3)') sep
      if(sep<10) then
        sfirst=index(snu,' ')+2
      else if(sep<100) then
        sfirst=index(snu,' ')+1
      else
        sfirst=1
      end if  

      write(rnu,'(i3)') rot
      if(rot<10) then
        rfirst=index(rnu,' ')+2
      else if(rot<100) then
        rfirst=index(rnu,' ')+1
      else
        sfirst=1
      end if  
    
      start_name='smin'//snu(sfirst:3)//'.'//rnu(rfirst:3)

!gamma_loop : do gam=1,ngamma  
      
 !       if(score_pos(npos)==0) cycle gamma_loop

        nor=nor+1
        molecule(:)=start_position(:)
        write(6,form_text) "original configuration" 
        call get_centers(.true.)
        call start_rotation(Lig_position)
        Start_Lig(:)=Lig_position(:)
        Old_Lig(:)=Lig_position(:)
        call energy(Start_Lig,Etot, Elj,Eelec,grad)
        write(6,*) 'Energy before relocation', Etot, Elj, Eelec

        x2=center(2)%x
        y2=center(2)%y
        z2=center(2)%z
        write(6,*)

        ps=real(gam-1)*2.0*pi/real(ngamma)

        do parti=1,Np2 
          i=prot_id(2)%Pstot_item(parti)
          xi=molecule(i)%x 
          yi=molecule(i)%y 
          zi=molecule(i)%z 

          dx=xi-x2
          dy=yi-y2
          dz=zi-z2


          xj=cos(ps)*(dz*sin(th2)+cos(th2)*(dx*cos(ph2)-dy*sin(ph2)))&
            -sin(ps)*(dy*cos(ph2)+dx*sin(ph2))

          yj=cos(ps)*(dy*cos(ph2)+dx*sin(ph2))&
            +sin(ps)*(dz*sin(th2)+cos(th2)*(dx*cos(ph2)-dy*sin(ph2)))

          zj=dz*cos(th2)-sin(th2)*(dx*cos(ph2)-dy*sin(ph2))

          molecule(i)%x=x2+Psep(sep)*vect_u1(sep)%x-Prot_sep*vector%x+xj
          molecule(i)%y=y2+Psep(sep)*vect_u1(sep)%y-Prot_sep*vector%y+yj
          molecule(i)%z=z2+Psep(sep)*vect_u1(sep)%z-Prot_sep*vector%z+zj
        end do 
         
        write(6,form_text) "After separation/rotation"
        call get_centers(.true.)
        call start_rotation(Lig_position)

!        if(art) then
!          write(6,form_tens) 'minimization before art'
!          call minimize(Etot,Elj,Eelec) 
!          write(96,form_dec) sep,rot,gam,Prot_sep,theta,phi,Lig_position(6),&
!                             Lig_position(4),Lig_position(5),Elj,Eelec,Etot
!          write(6,form_tens) 'starting activation/relaxation'
!          call art_protein(Etot,Elj,Eelec)
!          exit rotation_loop
!           exit
!        else
          write(6,form_tens) 'starting minimization', real(nor) 
          call minimize(Etot,Elj,Eelec) 
        
!        if(rot==1.and.gam==1) Emin(sep)=Etot
          if(npos==1) Ermin=Etot        

!        if(Etot<=Emin(sep)) then
          if(Etot<=Ermin) then
            nmin=npos
!          Emin(sep)=Etot
!          Emlj(sep)=Elj
!          Emelec(sep)=Eelec
            Ermin=Etot
            Erelec=Eelec
            Erlj=Elj
            tmin=theta
            pmin=phi
            Psmin=Prot_sep
            amin=Lig_position(6)
            bmin=Lig_position(4)
            gmin=Lig_position(5)
!          call write_pdb_file(2,start_name)
          end if 

          write(6,*) 'lower energy yet', nmin, Ermin 
!        end if 

!      end do gamma_loop
      write(96,form_dec) nsep,nrot,gam,Prot_sep,theta,phi,Lig_position(6),Lig_position(4),Lig_position(5),Elj,Eelec,Etot
!      write(95,form_dec) nsep,nrot,gam,Psmin,tmin,pmin,amin,bmin,gmin,Erlj,Erelec,Ermin
!    end do rotation_loop
 
!    call save_data(nsep)

    write(6,*) 'Energy evaluations during run: ', evalf_number
     
!  end do separation_loop

  end do

  999 continue

  return

end subroutine make_potential_map

end module mapping

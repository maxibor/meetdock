module format_declaration
  
  implicit none
   
  character*60 :: form_date="(1x,a24,i2,a1,i2,a1,i4,a4,i2,a1,i2,a1,i2,a10)"
  
  character*40 :: form_file="(1x,a22,1x,a40)"
  character*40 :: form_i   ="(1x,20i7)"
  character*40 :: form_r   ="(1x,20f13.6)"
  character*60 :: form_dec ="(1x,i4,1x,i6,1x,10f13.6)"
  character*40 :: form_c1  ="(1x,a52)"
  character*40 :: form_c2  ="(1x,a21)"
  
  character*40 :: form_tens="(1x,a40,1x,3f13.6)"
  character*40 :: form_talp="(1x,a35,1x,3es15.5)"

  character*40 :: form_text="(1x,a64)"
  
  character*80 :: form_pdb   ="(6x,i5,6x,a4,a1,i4,4x,3f8.3)"
  character*80 :: form_coord ="(30x,3f8.3)"
  character*80 :: form_prot  ="(a4,2x,i5,2x,a2,2x,a4,a1,i4,4x,3f8.3,6x,3f8.3)"
  character*80 :: form_line  ="(a)"
  character*80 :: form_zach  ="(1x,a14,2x,i3,2x,a5,2x,a1,2x,a9,2x,i5)" 

end module format_declaration

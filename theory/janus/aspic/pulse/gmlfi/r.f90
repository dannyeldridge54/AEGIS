program pr
  use infprec, only : kp
  use srflow, only : scalar_spectral_index, tensor_to_scalar_ratio, scalar_running
  use srreheat, only : Nzero
  use gmlfisr
  use gmlfireheat
  implicit none
  real(kp) :: x, xe, e(3), bf, P
  P = 2.1127e-9_kp; xe = gmlfi_x_endinf(2._kp,1._kp,0.01_kp)
  write(*,'(A,ES24.16)') 'NZ ', Nzero
  x = gmlfi_x_rrad(2._kp,1._kp,0.01_kp,xe, 0._kp, P, bf); e = (/gmlfi_epsilon_one(x,2._kp,1._kp,0.01_kp), gmlfi_epsilon_two(x,2._kp,1._kp,0.01_kp), gmlfi_epsilon_three(x,2._kp,1._kp,0.01_kp)/)
  write(*,'(A,A,F7.1,5ES24.15)') 'RT ', 'rrad ', 0.0, -bf, scalar_spectral_index(e), tensor_to_scalar_ratio(e), scalar_running(e), x
  x = gmlfi_x_rrad(2._kp,1._kp,0.01_kp,xe, -10._kp, P, bf); e = (/gmlfi_epsilon_one(x,2._kp,1._kp,0.01_kp), gmlfi_epsilon_two(x,2._kp,1._kp,0.01_kp), gmlfi_epsilon_three(x,2._kp,1._kp,0.01_kp)/)
  write(*,'(A,A,F7.1,5ES24.15)') 'RT ', 'rrad ', -10.0, -bf, scalar_spectral_index(e), tensor_to_scalar_ratio(e), scalar_running(e), x
  x = gmlfi_x_star(2._kp,1._kp,0.01_kp,xe, 0._kp, -100._kp, P, bf); e = (/gmlfi_epsilon_one(x,2._kp,1._kp,0.01_kp), gmlfi_epsilon_two(x,2._kp,1._kp,0.01_kp), gmlfi_epsilon_three(x,2._kp,1._kp,0.01_kp)/)
  write(*,'(A,A,F7.1,5ES24.15)') 'RT ', 'rhow ', -100.0, -bf, scalar_spectral_index(e), tensor_to_scalar_ratio(e), scalar_running(e), x
  x = gmlfi_x_star(2._kp,1._kp,0.01_kp,xe, 0._kp, -150._kp, P, bf); e = (/gmlfi_epsilon_one(x,2._kp,1._kp,0.01_kp), gmlfi_epsilon_two(x,2._kp,1._kp,0.01_kp), gmlfi_epsilon_three(x,2._kp,1._kp,0.01_kp)/)
  write(*,'(A,A,F7.1,5ES24.15)') 'RT ', 'rhow ', -150.0, -bf, scalar_spectral_index(e), tensor_to_scalar_ratio(e), scalar_running(e), x
end program pr

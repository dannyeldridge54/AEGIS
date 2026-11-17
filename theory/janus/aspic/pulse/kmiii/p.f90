program pp
  use infprec, only : kp
  use srflow, only : scalar_spectral_index, tensor_to_scalar_ratio, scalar_running
  use kmiiisr
  implicit none
  real(kp) :: Ns(2) = (/50._kp, 60._kp/), x, xe, e(3), x60, xf, xx
  integer :: j, k
  xe = kmiii_x_endinf(1e10_kp,1e4_kp)
  do j = 1, 2
    x = kmiii_x_trajectory(-Ns(j), xe,1e10_kp,1e4_kp); if (j == 2) x60 = x
    e = (/kmiii_epsilon_one(x,1e10_kp,1e4_kp), kmiii_epsilon_two(x,1e10_kp,1e4_kp), kmiii_epsilon_three(x,1e10_kp,1e4_kp)/)
    write(*,'(A,F5.1,6ES24.15)') 'PT ', Ns(j), x, scalar_spectral_index(e), tensor_to_scalar_ratio(e), scalar_running(e), xe, e(1)
  end do
  xf = x60 + 4._kp*(x60 - xe)
  do k = 0, 3999
    xx = xe + (xf - xe)*real(k,kp)/3999._kp
    write(*,'(A,3ES24.15)') 'VG ', xx, kmiii_norm_potential(xx,1e10_kp,1e4_kp), kmiii_norm_deriv_potential(xx,1e10_kp,1e4_kp)
  end do
end program pp

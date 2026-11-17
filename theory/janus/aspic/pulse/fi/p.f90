program pp
  use infprec, only : kp
  use srflow, only : scalar_spectral_index, tensor_to_scalar_ratio, scalar_running
  use fisr
  implicit none
  real(kp) :: Ns(2) = (/50._kp, 60._kp/), x, xe, e(3), x60, xf, xx
  integer :: j, k
  xe = fi_x_endinf(1e-6_kp,1._kp)
  do j = 1, 2
    x = fi_x_trajectory(-Ns(j), xe,1e-6_kp,1._kp); if (j == 2) x60 = x
    e = (/fi_epsilon_one(x,1e-6_kp,1._kp), fi_epsilon_two(x,1e-6_kp,1._kp), fi_epsilon_three(x,1e-6_kp,1._kp)/)
    write(*,'(A,F5.1,6ES24.15)') 'PT ', Ns(j), x, scalar_spectral_index(e), tensor_to_scalar_ratio(e), scalar_running(e), xe, e(1)
  end do
  xf = x60 + 4._kp*(x60 - xe)
  do k = 0, 3999
    xx = xe + (xf - xe)*real(k,kp)/3999._kp
    write(*,'(A,3ES24.15)') 'VG ', xx, fi_norm_potential(xx,1e-6_kp,1._kp), fi_norm_deriv_potential(xx,1e-6_kp,1._kp)
  end do
end program pp

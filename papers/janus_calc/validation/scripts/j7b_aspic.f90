program j7b
  use infprec, only : kp
  use srflow, only : scalar_spectral_index, tensor_to_scalar_ratio, scalar_running
  use dwisr, only : dwi_x_endinf, dwi_x_trajectory, dwi_epsilon_one, dwi_epsilon_two, dwi_epsilon_three
  use esisr, only : esi_x_endinf, esi_x_trajectory, esi_epsilon_one, esi_epsilon_two, esi_epsilon_three
  use kmiisr, only : kmii_x_endinf, kmii_x_trajectory, kmii_epsilon_one, kmii_epsilon_two, kmii_epsilon_three
  use lfisr, only : lfi_x_endinf, lfi_x_trajectory, lfi_epsilon_one, lfi_epsilon_two, lfi_epsilon_three
  use lisr, only : li_x_endinf, li_x_trajectory, li_epsilon_one, li_epsilon_two, li_epsilon_three
  use mhisr, only : mhi_x_endinf, mhi_x_trajectory, mhi_epsilon_one, mhi_epsilon_two, mhi_epsilon_three
  use nisr, only : ni_x_endinf, ni_x_trajectory, ni_epsilon_one, ni_epsilon_two, ni_epsilon_three
  use rgisr, only : rgi_x_endinf, rgi_x_trajectory, rgi_epsilon_one, rgi_epsilon_two, rgi_epsilon_three
  use sfisr, only : sfi_x_endinf, sfi_x_trajectory, sfi_epsilon_one, sfi_epsilon_two, sfi_epsilon_three
  use sisr, only : si_x_endinf, si_x_trajectory, si_epsilon_one, si_epsilon_two, si_epsilon_three
  implicit none
  real(kp) :: Ns(2) = (/50._kp, 60._kp/), x, xe, e(3), t0, t1
  integer :: i, j, rep
  do i = 1, 17
  do j = 1, 2
  call cpu_time(t0)
  do rep = 1, 1000
  select case (i)
  case (1)
    xe = lfi_x_endinf(2._kp); x = lfi_x_trajectory(-Ns(j), xe,2._kp)
    e = (/lfi_epsilon_one(x,2._kp), lfi_epsilon_two(x,2._kp), lfi_epsilon_three(x,2._kp)/)
  case (2)
    xe = lfi_x_endinf(4._kp); x = lfi_x_trajectory(-Ns(j), xe,4._kp)
    e = (/lfi_epsilon_one(x,4._kp), lfi_epsilon_two(x,4._kp), lfi_epsilon_three(x,4._kp)/)
  case (3)
    xe = lfi_x_endinf(2._kp/3._kp); x = lfi_x_trajectory(-Ns(j), xe,2._kp/3._kp)
    e = (/lfi_epsilon_one(x,2._kp/3._kp), lfi_epsilon_two(x,2._kp/3._kp), lfi_epsilon_three(x,2._kp/3._kp)/)
  case (4)
    xe = si_x_endinf(); x = si_x_trajectory(-Ns(j), xe)
    e = (/si_epsilon_one(x), si_epsilon_two(x), si_epsilon_three(x)/)
  case (5)
    xe = ni_x_endinf(5._kp); x = ni_x_trajectory(-Ns(j), xe,5._kp)
    e = (/ni_epsilon_one(x,5._kp), ni_epsilon_two(x,5._kp), ni_epsilon_three(x,5._kp)/)
  case (6)
    xe = ni_x_endinf(10._kp); x = ni_x_trajectory(-Ns(j), xe,10._kp)
    e = (/ni_epsilon_one(x,10._kp), ni_epsilon_two(x,10._kp), ni_epsilon_three(x,10._kp)/)
  case (7)
    xe = esi_x_endinf(1._kp); x = esi_x_trajectory(-Ns(j), xe,1._kp)
    e = (/esi_epsilon_one(x,1._kp), esi_epsilon_two(x,1._kp), esi_epsilon_three(x,1._kp)/)
  case (8)
    xe = mhi_x_endinf(10._kp); x = mhi_x_trajectory(-Ns(j), xe,10._kp)
    e = (/mhi_epsilon_one(x,10._kp), mhi_epsilon_two(x,10._kp), mhi_epsilon_three(x,10._kp)/)
  case (9)
    xe = kmii_x_endinf(2._kp); x = kmii_x_trajectory(-Ns(j), xe,2._kp)
    e = (/kmii_epsilon_one(x,2._kp), kmii_epsilon_two(x,2._kp), kmii_epsilon_three(x,2._kp)/)
  case (10)
    xe = rgi_x_endinf(1._kp); x = rgi_x_trajectory(-Ns(j), xe,1._kp)
    e = (/rgi_epsilon_one(x,1._kp), rgi_epsilon_two(x,1._kp), rgi_epsilon_three(x,1._kp)/)
  case (11)
    xe = dwi_x_endinf(25._kp); x = dwi_x_trajectory(-Ns(j), xe,25._kp)
    e = (/dwi_epsilon_one(x,25._kp), dwi_epsilon_two(x,25._kp), dwi_epsilon_three(x,25._kp)/)
  case (12)
    xe = sfi_x_endinf(2._kp,20._kp); x = sfi_x_trajectory(-Ns(j), xe,2._kp,20._kp)
    e = (/sfi_epsilon_one(x,2._kp,20._kp), sfi_epsilon_two(x,2._kp,20._kp), sfi_epsilon_three(x,2._kp,20._kp)/)
  case (13)
    xe = li_x_endinf(0.3_kp); x = li_x_trajectory(-Ns(j), xe,0.3_kp)
    e = (/li_epsilon_one(x,0.3_kp), li_epsilon_two(x,0.3_kp), li_epsilon_three(x,0.3_kp)/)
  case (14)
    xe = esi_x_endinf(sqrt(2._kp)); x = esi_x_trajectory(-Ns(j), xe,sqrt(2._kp))
    e = (/esi_epsilon_one(x,sqrt(2._kp)), esi_epsilon_two(x,sqrt(2._kp)), esi_epsilon_three(x,sqrt(2._kp))/)
  case (15)
    xe = ni_x_endinf(7._kp); x = ni_x_trajectory(-Ns(j), xe,7._kp)
    e = (/ni_epsilon_one(x,7._kp), ni_epsilon_two(x,7._kp), ni_epsilon_three(x,7._kp)/)
  case (16)
    xe = lfi_x_endinf(3._kp); x = lfi_x_trajectory(-Ns(j), xe,3._kp)
    e = (/lfi_epsilon_one(x,3._kp), lfi_epsilon_two(x,3._kp), lfi_epsilon_three(x,3._kp)/)
  case (17)
    xe = lfi_x_endinf(1._kp); x = lfi_x_trajectory(-Ns(j), xe,1._kp)
    e = (/lfi_epsilon_one(x,1._kp), lfi_epsilon_two(x,1._kp), lfi_epsilon_three(x,1._kp)/)
  end select
  end do
  call cpu_time(t1)
  write(*,'(I3,1X,F5.1,1X,ES22.14,1X,ES22.14,1X,ES22.14,1X,ES22.14,1X,ES22.14,1X,ES12.4)') i, Ns(j), x, &
     scalar_spectral_index(e), tensor_to_scalar_ratio(e), scalar_running(e), xe, (t1-t0)/1000._kp
  end do
  end do
end program j7b

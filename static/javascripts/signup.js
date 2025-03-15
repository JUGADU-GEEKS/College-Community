sendOTPBtn = document.body.querySelector('.sendotp')
OTPdiv = document.body.querySelector('.otp')

sendOTPBtn.addEventListener("click", (e)=>{
    OTPdiv.style.display = "block";
})
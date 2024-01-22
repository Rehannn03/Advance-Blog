const Hero = () => {
  return (
    <div className="flex flex-col bg bg-heroBG bg-cover h-screen w-screen">
      {/* Text and button ??? */}
      <div className="w-[600px] h-[171px]">
        <p className="relative w-[600px] h-[171px] top-[150px] left-[180px] [font-family:'Roboto-Regular',Helvetica] font-normal text-transparent text-[64px] tracking-[0] leading-[normal]">
          <span className="text-[#6f61c0] w-48">Don’t&nbsp;Stop</span>
          <span className="[font-family:'Inter-Regular',Helvetica] text-black">
            &nbsp;
            &nbsp;
          </span>
          <span className="[font-family:'Roboto_Mono-Medium',Helvetica] font-medium text-black text-[96px] items-start">
            Reading.
          </span>
        </p>
      </div>
    </div>
  );
};

export default Hero;

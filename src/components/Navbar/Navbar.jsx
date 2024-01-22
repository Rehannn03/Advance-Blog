import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { navLinks } from "../../constants";


export function Navbar() {
  const [active, setActive] = useState("");
  const [toggle, setToggle] = useState(false);
  return (
    <div className=" flex flex-row w-screen h-[100px] bg-[#d5ffe4] sticky top-0">
      {/* logo and title */}
      <div className="flex flex-row ml-40">
        <Link
          to="/"
          className=" flex items-center gap-2"
          onClick={() => {
            setActive("");
            window.scrollTo(0, 0);
          }}
        >
          <img src="/logo.png" width={100} height={50} />
          <h1 className="flex justify-center items-center [font-family:'Montserrat-ExtraBold',Helvetica] font-extrabold text-black text-[36px]">
            Blogy Wogy
          </h1>
        </Link>
      </div>
      {/* Nav Items */}
      <div className="flex flex-row items-center ml-[450px]">
        <ul className="list-none hidden sm:flex flex-row gap-10">
          {navLinks.map((link) => (
            <li
              key={link.id}
              className={`${
                active === link.title ? "text-white" : "text-black    "
              } hover:text-[#6F61C0] text-[30px]
              font-medium cursor-pointer
              `}
              onClick={() => {
                setActive(link.title);
              }}
            >
              <Link
              to={`${link.id}`}
              >
                {link.title}
              </Link>
             
            </li>
          ))}
        </ul>
        <div className="sm:hidden flex flex-1 justify-end items-center">
          <img
            src={toggle ? menu : close}
            alt="menu"
            className="w-[28px] h-[28px] 
            object-contain cursor-pointer"
            onClick={() => setToggle(!toggle)}
          />
          <div
            className={`${!toggle ? "hidden" : "flex"} 
          p-6 black-gradient absolute top-20 right-0 mx-4 
          my-2 min-w-[140px] z-10 rounded-xl
          }`}
          >
            <ul className="list-none flex justify-end items-start flex-col gap-4">
              {navLinks.map((link) => (
                <li
                  key={link.id}
                  className={`${
                    active === link.title ? "text-white" : "text-secondary"
                  } text-[##6F61C0] font-poppins
              font-medium text-[16px]
              `}
                  onClick={() => {
                    setToggle(!toggle);
                    setActive(link.title);
                  }}
                >
                  <a href={`#${link.id}`}>{link.title}</a>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};


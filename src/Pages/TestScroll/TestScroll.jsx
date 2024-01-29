import { useState, useEffect, useRef } from "react";
import { useIntersectionObserver } from "../../hooks/useIntersectionObserver";

const limit = 9;

const TestScroll = () => {
  const [data, setData] = useState([]);
  const [isError, setIsError] = useState(false);
  const [isInitialFetch, setIsInitialFetch] = useState(false);

  const pageRef = useRef(1);
  const [hasMore, setHasMore] = useState(false);

  const fetchPosts = async ({ page, isFetchingFirstTime }) => {
    try {
      setIsError(false);
      isFetchingFirstTime && setIsInitialFetch(true);

      const resPro = await fetch(
        `https://dummyjson.com/products?limit=${limit}&skip=${
          (page - 1) * limit
        }`
      );

      const data = await resPro.json();

      if (data.products) {
        setData((prev) => {
          const newData = [...prev, ...data.products];

          if (newData.length < data.total) {
            setHasMore(true);
          } else setHasMore(false);

          return newData;
        });
      } else {
        setHasMore(false);
      }
    } catch (err) {
      setHasMore(false);
      setIsError(true);
    } finally {
      setIsInitialFetch(false);
    }
  };

  // Initial fetch
  useEffect(() => {
    fetchPosts({ page: pageRef.current, isFetchingFirstTime: true });
  }, []);

  // Infinite scrolling
  const [targetRef, isIntersecting] = useIntersectionObserver({ threshold: 1 });

  useEffect(() => {
    if (hasMore && isIntersecting) {
      pageRef.current = pageRef.current + 1;
      fetchPosts({ page: pageRef.current });
    }
    console.log(data)
  }, [isIntersecting, hasMore]);
  return(
    // This Shit just loads a list with title only... Used for teting infinite Scrolling    
    // <div>
    //     <div>
    //     {data.map((data) => (
    //         <li key={data.id}>
    //             {data.title}
    //         </li>
    //     )) }
    //     </div>
    //     {hasMore && (
    //     <div ref={targetRef}>
    //       Loaind
    //     </div>
    //   )}
    // </div>

    <div className=" flex justify-center items-center">
        {isError ? (<h1>failed to fetch</h1>): (
            <div className="grid grid-cols-3 gap-5">
                {data.map((data) => (
                    <li key={data.id} className="w-[300px] h-auto bg-red-500 m-3 container text-sm list-none text-center">
                        <img src={data.thumbnail} alt="Vivek Ki photo" height={300} width={300}/>
                        {data.title} <br />
                        {data.description}
                    </li>
                ))}
                {hasMore && (
                    <div ref={targetRef}>
                        Loadin
                </div>)}

            </div>
        )}
    </div>
  )
}

export default TestScroll;
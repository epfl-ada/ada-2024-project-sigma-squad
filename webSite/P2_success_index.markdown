---
layout: page
title: Success index 
permalink: /success/
---

# Movie success index 
In order to access and define actors carrers, they fiirst had to  answer a crucial question : **“What makes a movie truly successful?”**

Around a beer at Sat, hey were debating it: 

> “**Profit!**” shouted Mathieu,who dreamed about becoming a milionair star since 3 years old.
>
> “No way, it’s about **revenue**.” countered Maël, who’d seen Avengers too many times to think otherwise.
>
> “**Reviews!**” argued Aiden.  “If IMDb doesn’t like it, I don’t like it.”
>
> “**Oscars** matter, though,” whispered Elise, as Pol nodded solemnly, “Nobody argues with gold statues.”

To settle the debate, the friends decided to design the **Movie Success Index**—a system to rank movies based on **profitability**, **revenue**, **reviews**, and **Oscar nominations**.

Since they had been paying close attention during their ADA lectures, they knew that the data needed a bit of transformation to make it both meaningful and usable.

- For the **profitability factor**, Mathieu used the data on revenue and budget to calculate the ratio. However, even though Mathieu’s eyes sparkled at the sight of massive revenue numbers, he knew that to scale everything correctly from 0 to 10, he had to apply a log transformation. This smoothed out the extreme values caused by colossal blockbusters.

- For the **revenue factor**, Maël took charge:  
  *“Box office revenue is massive, but we log-transformed it too. Otherwise, Avatar would crush everything forever. This way, even low-budget hits look respectable.”*

Now, both profitability and revenue were neatly scaled from 0 to 10.

- Aiden, the IMDb enthusiast, happily handled the **reviews factor**, as ratings were already graded from 0 to 10.  
  *“Done and dusted. What a day!”* he exclaimed.

- Finally, Pol and Elise tackled the **oscar nomination factor**. Since a movie with many nominations already speaks for itself, they applied a log scale to ensure that each additional nomination added less weight. This way, the oscars boosted the index without overwhelming it.

---


<iframe src="/assets/plots/oscar_nomination_distribution.html" width="100%" height="600" frameborder="0"></iframe>

FAIRE TEXT - IMAGE MEME LIGNE AVCE GRAOHE DE CHAQUE FACTOR ? 
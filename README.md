# amlab parts

**Hi, guys!**

Usually, my work is my personal project. I can not to show all several dozen thousands line of codes that were write by me. But there is a good thing, I can show small parts of projects, for example [amlab.me](https://amlab.me). It's not perfect code it's real code. It will be enough for an understanding of my skills.

*So, get a cup of tea and let's start!*

---

There are just several modules that show the different part of the works. A deploying is not includes in README because I think you are looking for a python developer. Of course, you can see deploying too. It can be interesting enough!

---

**The first** is `bots.core.telegram`. Every company must have a bot! So, our products think the same. It's the most fully part of modules and I think it's the most interesting because you find a lot of patters, *live comments* and tests.

**The second** is `amlabcore.external`. Amlab has a lot of integrations with external service like Mandrill, Cloudpayments, GetResponse, Slack, Telegram, Hubspot, Yandex.Disk etc. A new integration is appearing every month. This way it was strong necessary to implement an easier mechanism for sending and logging requests.

The `amlabcore.tests` has a part of a common test. I think when a docker container is running via pytest on developer machine is cool (:

**The third** is `slack.source`. The harder part of working with external API is assembling a message. It's interesting that Slack team has a library for python but it's just to send requests without assembling a message. So, as you will see recursion is the greatest human invention!

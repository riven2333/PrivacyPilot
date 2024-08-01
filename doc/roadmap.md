At the very first stage, we will enable some useful workflow plugins that are better deployed locally.
Specifically, these plugins are:

- [x] Local Python code interpreter (make it possible for agent to take action locally)
- [x] Local file search (to help the code interpreter work better)
- [ ] Local RAG support (to help potential local/remote LLM Agent learn more about private information in a privacy-secure way)
- [ ] Local slides generation (an example plugin to boost workflow locally; agent can use local information from file_search or RAG, then generate slides)

The next step is towards seamless installation (one-click installer with `embedded Python interpreter`) and enriching the auto operation on PC (maybe for Windows first with `pywinauto`).
- [ ] one-click installer with `embedded Python interpreter`
- [ ] windows automation with `pywinauto`

Some other ideas with lower priorities are here:
- [ ] Privacy protection for interaction between **Agent** and **Plugin**
- [ ] Complete user query and act locally like [UFO](https://github.com/microsoft/UFO)
- [ ] Light-weight UI for simple chat with local Agent, a UI example is [G-assist](https://www.nvidia.cn/geforce/news/gfecnt/20246/g-assist-ai-assistant/)
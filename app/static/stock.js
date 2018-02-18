var app new Vue({
    el:'#order',
    data:{
        message: axios.get('/api/stock/',{
            params:{
                id:2
            }
        }),
        todos: [
      { text: '学习 JavaScript' },
      { text: '学习 Vue' },
      { text: '整个牛项目' }
    ]
    },
    delimiters: ['[[',']]']
    
});

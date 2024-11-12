/**function to check if metamask in installed */
const checkInstalled = () => {
  if (typeof window.ethereum == 'undefined') {
    return false;
  } else {
    $('#metamask').on('click', connectWithMetamask);
    return true;
  }
}

/** Function to connect to metamask */
const connectWithMetamask = async () => {
  // A Web3Provider wraps a standard Web3 provider, which is
  // what MetaMask injects as window.ethereum into each page
  window.provider = new ethers.providers.Web3Provider(window.ethereum);
  // MetaMask requires requesting permission to connect users accounts
  const accounts = await provider.send("eth_requestAccounts", []);
  const address = await accounts[0];

  // The MetaMask plugin also allows signing transactions to
  // send ether and pay to change state within the blockchain.
  // For this, you need the account signer...
  const signer = provider.getSigner()

  const page = window.location.pathname;
  if (page === '/login') {
    const form = document.getElementById('login_form');
    const formData = new FormData(form);
    formData.append('web3_address', address);
    formData.append('account_type', '1');
    try {
      const response = await fetch(window.location.pathname, {
        method: "POST",
        body: formData,
      })
      const data = await response.json();
      if (data.success) {
        window.location.href = window.location.pathname.replace('/login', '/dashboard');
      }
    } catch (e) {
      console.error(e);
    }
  } else if (page === '/register') {
    const wallet = createWallet();
    $('#f_name').val("EOA");
    $('#l_name').val("EOA");
    $('#email').val(address + "@internal.kitchenmanager");
    $('#password').val("metamask");
    $('#confirm_password').val("metamask");
    const form = document.getElementById('register_form');
    const formData = new FormData(form);
    formData.append('google_id', "EOA");
    formData.append('account_type', '1');
    formData.append('mnemonic', "EOA");
    formData.append('priv', "EOA");
    formData.append('web3_address', address);
    try {
      const response = await fetch(window.location.pathname, {
        method: "POST",
        body: formData,
      })
      const data = await response.json();
      if (data.success) {
        window.location.href = window.location.pathname.replace('/register', '/login');
      }
    } catch (e) {
      console.error(e);
    }
  } 
}

/**
* Function to handle Google Signin response
* @param {*} response 
*/
async function handleCredentialResponse(response) {
  const page = window.location.pathname;
  const userCredential = decodeJWT(response.credential);
  if (page === '/login') {
    const form = document.getElementById('login_form');
    const formData = new FormData(form);
    formData.append('google_id', userCredential.sub);
    formData.append('account_type', '3');
    try {
      const response = await fetch(window.location.pathname, {
        method: "POST",
        body: formData,
      })
      const data = await response.json();
      if (data.success) {
        window.location.href = window.location.pathname.replace('/login', '/dashboard');
      }
    } catch (e) {
      console.error(e);
    }

  } else if (page === '/register') {
    const wallet = createWallet();
    $('#f_name').val(userCredential.given_name);
    $('#l_name').val(userCredential.family_name);
    $('#email').val(userCredential.email);
    $('#password').val("googleaccount");
    $('#confirm_password').val("googleaccount");
    const form = document.getElementById('register_form');
    const formData = new FormData(form);
    formData.append('google_id', userCredential.sub);
    formData.append('account_type', '3');
    formData.append('mnemonic', wallet.mnemonic.phrase);
    formData.append('priv', wallet.privateKey);
    formData.append('web3_address', wallet.address);
    try {
      const response = await fetch(window.location.pathname, {
        method: "POST",
        body: formData,
      })
      const data = await response.json();
      if (data.success) {
        window.location.href = window.location.pathname.replace('/register', '/login');
      }
    } catch (e) {
      console.error(e);
    }
  }
}

/**
 * Function to decode Google user credentials
 * @param {*} credential 
 * @returns 
 */
const decodeJWT = (credential) => {
  var tokens = credential.split('.');
  return JSON.parse(atob(tokens[1]));
}

/**
 * Function to create a new wallet
 * @returns {ethers.Wallet}
 */
const createWallet = () => {
  const wallet = ethers.Wallet.createRandom()
  return wallet;
}

const submitRegisterForm = async () => {
  const form = document.getElementById('register_form');
  const formData = new FormData(form);
  if (
    formData.get('password') === formData.get('confirm_password')
    && formData.get('email') !== ''
    && formData.get('password') !== ''
  ) {
    try {
      const wallet = createWallet();
      formData.append('web3_address', wallet.address)
      formData.append('mnemonic', wallet.mnemonic.phrase)
      formData.append('priv', wallet.privateKey)
      formData.append('account_type', '2')
      formData.append('google_id', 'EOA')
      const response = await fetch(window.location.pathname, {
        method: "POST",
        body: formData,
      })
      const data = await response.json();
      if (data.success) {
        window.location.href = window.location.pathname.replace('/register', '/login');
      }
    } catch (e) {
      console.error(e);
    }
  }
}

const submitLoginForm = async () => {
  const form = document.getElementById('login_form');
  const formData = new FormData(form);
  if  (formData.get('email') !== '' && formData.get('password') !== '')  {
    try  {
      formData.append('account_type', '2')
      const response = await fetch(window.location.pathname,  {
        method:  "POST",
        body: formData,
      })
      const data = await response.json();
      if  (data.success)  {
        window.location.href = window.location.pathname.replace('/login', '/dashboard');
      }
    } catch  (e)  {
      console.error(e);
    }
  }
}


/**
 * Function to submit a new recipe form
 */
const submitRecipeForm = async () => {
  form = document.getElementById('create_recipe_form');
  formData = new FormData(form);
  const name = formData.get('name');
  const description = formData.get('description');
  const itemkind = formData.get('itemkind');
  if ((itemkind != null) && (name != '') && (description != '')) {
    try {
      const response = await fetch("/chef/createrecipe", {
        method: "POST",
        // Set the FormData instance as the request body
        body: formData,
      })
      const data = await response.json();
      if (data.success) {
        window.location.href = "/chef/createrecipe";
      }
    } catch (e) {
      console.error(e);
    }
  } else {
    alert('Make sure you selected a kind of item and give name and description');
  }
}

const submitPlaceOrderForm = async () => {
  const form = document.getElementById('place_order_form');
  const formData = new FormData(form);
  try {
    const response = await fetch(window.location.pathname, {
      method: "POST",
      // Set the FormData instance as the request body
      body: formData,
    })
    const data = await response.json();
    if (data.success) {
      window.location.href = window.location.pathname;
    }
  } catch (e) {
    console.error(e);
  }
}

const submitAddDeliveryForm = async () => {
  const form = document.getElementById('add_delivery_form');
  console.log(form)
  const formData = new FormData(form);
  try {
    const response = await fetch(window.location.pathname, {
      method: "POST",
      body: formData,
    })
    const data = await response.json();
    if (data.success) {
      window.location.href = window.location.pathname;
    }
  } catch (e) {
    console.error(e);
  }
}

const submitEditRecipeForm = async () =>  {
  const form = document.getElementById('edit-recipe-form');
  const formData = new FormData(form);
  if (formData.get('sellable_item_checkbox') == 'on') {
    formData.append('sellable_item', true);
  } else {
    formData.append('sellable_item', false);
  }
  try  {
    const response = await fetch(window.location.pathname + '/edit', {
      method:  "POST",
      body: formData,
    })
    const data = await response.json();
    
    window.location.reload()
    
  } catch  (e)  {
    console.error(e);
  }
}

const editRecipe = () => {
  $('#autocomplete-input').attr('disabled', false)
  if (is_chef == "True") {
    const ingredients = $('.myCheckbox')
    for (let ingredient of ingredients) {
      $(ingredient).prop('disabled', false)
      children = $(ingredient).parent().parent().next().children()
      $(children[0]).prop('disabled', false)
      $('#portions').prop('disabled', false)
    }
  }
  if (is_manager == "True") {
    $('#name').prop('disabled', false)
    $('#description').prop('disabled', false)
    $('#sellable_item_checkbox').prop('disabled', false)
    $('#price').prop('disabled', false)
  }
  $('label').addClass('brown-text',"text-darken-4")
  $('#submitform').prop('disabled', false);
    const inputFields = $('.view-toggle');
    for (let inputField of inputFields) {
      $(inputField).hide();
    }
    $('input[type=checkbox]').on('change', function () {
      const id = $(this).attr('id');
      if (id.includes("manufactored")) {
        itemId = '#manufactored_ingredient_quantity_' + id.split('_')[2];
      } else {
        itemId = '#ingredient_quantity_' + id.split('_')[1];
      }
      if ($(this).is(':checked')) {
        $(itemId).parent().show();
      } else {
        $(itemId).prop('value', 0)
        $(itemId).parent().hide();
      }
    });
  $('#submitform').on('click', submitEditRecipeForm)
}

const submitWastageForm = async () => {
  form = document.getElementById('add_wastages_form');
  formData = new FormData(form);
  const info = document.getElementById('info')
  if (info != null) {
    try {
      const response = await fetch("/manager/addwastages", {
        method: "POST",
        // Set the FormData instance as the request body
        body: formData,
      })
      const data = await response.json();
      if (data.success) {
        window.location.href = "/manager/addwastages";
      }
    } catch (e) {
      console.error(e);
    }
  } else {
    alert('Make sure you add some info');
  }
}

const submitPrepareRecipeForm = async () =>  {
  const url = window.location.pathname.replace('manager', 'chef') + '/prepare'
  form = document.getElementById('add_preparation_form');
  formData = new FormData(form);
  try {
    const response = await fetch(url, {
      method: "POST",
      // Set the FormData instance as the request body
      body: formData,
    })
    const data = await response.json();
    if (data.success) {
      window.location.href = "/manager/recipes";
    }
  } catch (e) {
    console.error(e);
  }
}

const submitHireForm = async () =>  {
  const form = document.getElementById('hire-form');
  const formData = new FormData(form);
  const id = $('#user').html().split(" - ")[0]
  formData.append('id', id)
  formData.get('role')
  
  try {
    const response = await fetch(window.location.pathname, {
      method: "POST",
      // Set the FormData instance as the request body
      body: formData,
    })
    const data = await response.json();
    if (data.success) {
      window.location.href = "/manager/staff";
    }
  } catch (e) {
    console.error(e);
  }
}

const submitOrderForm = async () => {
  const form = document.getElementById('send-order');
  const formData = new FormData(form);
  try {
    const response = await fetch("/placedorders/"+orderId+"/send",  {
      method: "POST",
      // Set the FormData instance as the request body
      body: formData,
    })
    const data = await response.json();
    if (await data.success) {
      window.location.reload();
    }
  } catch (e) {
    console.error(e);
  }
}

let recipes;
let placedorders;
let deliveries;
let orders;
let wastages;
let stockTakes
let preparations;
let ingredient;
let manufactored_ingredient;

const getIngredientData = async (ingredient_id) => {
  try {
    const response = await fetch(`/api/ingredients/${ingredient_id}/get_ingredient_data`, {
      method:  "GET",
    })
    const data = await response.json();
    recipes = createRelatedRecipeRecords(await data['recipes'])
    placedorders = createRelatedPlacedOrderRecords(await data['placedorders'])
    deliveries = createRelatedDeliveryRecords(await data['deliveries'])
    wastages = createRelatedWastageRecords(await data['wastages'])
    stockTakes = createRelatedStockTakeRecords(await data['stock_takes'])
    ingredient = await data['ingredient']
    preparations = undefined
    orders = undefined
    displayIngredientData()
    $('#go_to').attr('disabled', true)
    $('#add_to_order').attr('disabled', false)
    $('#add_to_order').on('click', addToOrder)
  } catch (error) {
    
  }
}

const getManufactoredIngredientData = async (ingredient_id) => {
  try {
    const response = await fetch(`/api/manufactoredingredients/${ingredient_id}/get_ingredient_data`, {
      method:  "GET",
    })
    const data = await response.json();
    recipes = createRelatedRecipeRecords(await data['recipes'])
    orders = createRelatedOrderRecords(await data['orders'])
    wastages = createRelatedWastageRecords(await data['wastages'])
    preparations = createRelatedPreparationRecords(await data['preparations'])
    stockTakes = createRelatedStockTakeRecords(await data['stock_takes'])
    manufactored_ingredient = await data['ingredient']
    deliveries = undefined
    placedorders = undefined
    displayIngredientData()
    $('#add_to_order').attr('disabled', true)
    $('#go_to').attr('disabled', false)
    $('#go_to').on('click', goToRecipe)

  } catch (error) {
    
  }
}

const goToRecipe = () => {
  window.location.href = "/manager/recipes/" + ingredient['recipe']
}

const displayIngredientData = () => {
  $('#name').html(ingredient.name)
  $('#description').html(ingredient.description)
  $('#stock').parent().find("label").addClass('active')
  $('#stock').val(Number(ingredient.stock))
  $('#stock').attr('disabled', false)
  $("#recipes").html(recipes)
  $("#placed_orders").html(placedorders)
  $("#deliveries").html(deliveries)
  $("#preparations").html(preparations)
  $("#watages").html(wastages)
  $("#stock_takes").html(stockTakes)
  $("#sales").html(orders)
}

const switchGetIngredientData = (id, manufactored, name) => {
  $('#stock_take').attr('disabled', false)
  $('#stock_take').on('click', switchSetStock)
  if (window.location.pathname == "/manager/stockmanagement") {
    if (!manufactored)  {
      getIngredientData(id)
      $('.ingredient-only').show()
      $('.manufactored-only').hide() 
    } else  {
      getManufactoredIngredientData(id)
      $('.manufactored-only').show() 
      $('.ingredient-only').hide()
    }
  } else { 
    addIngredientQuantity(manufactored, id, name)
  }
}

const showTabData = (tabId) => {
  console.log(tabId,placedorders)
  if (tabId == 0 && recipes != undefined) {
    tab = document.getElementById('recipes')
    tab.innerHTML = ''
    tab.appendChild(recipes)
  } else if  (tabId == 1 && placedorders != undefined)  {
    console.log(placedorders)
    tab = document.getElementById('placedorders')
    tab.innerHTML = ''
    tab.appendChild(placedorders)
  } else if  (tabId == 2 && deliveries != undefined)  {
    tab = document.getElementById('deliveries')
    tab.innerHTML = ''
    tab.appendChild(deliveries)
  } else if (tabId == 3 && preparations != undefined) {
    tab = document.getElementById('preparations')
    tab.innerHTML = ''
    tab.appendChild(preparations)
  } else if (tabId == 4  && wastages != undefined) {
    tab = document.getElementById('wastages')
    tab.innerHTML = ''
    console.log(wastages)
    tab.appendChild(wastages)
  } else if  (tabId == 5  && stockTakes  != undefined)  {
    tab = document.getElementById('stocktakes')
    tab.innerHTML = ''
    tab.appendChild(stockTakes)
  } else if  (tabId == 6  && orders  != undefined)  {
    tab = document.getElementById('orders')
    tab.innerHTML = ''
    tab.appendChild(orders)
   }
}

const createRelatedOrderRecords = (data) => {
  let div = document.createElement('div')
  div.classList.add('container-fluid')
  let h5 = document.createElement('h5')
  h5.classList.add('text-center')
  h5.innerHTML = 'Releated sales'
  div.appendChild(h5)
  let ul = document.createElement('ul')
  ul.classList.add('list-group')
  if(data != [] && data != undefined){
    for (let sale of data) {
    let li = document.createElement('li')
    li.classList.add('list-group-item')
    li.innerHTML = 'Date: ' + sale.date + ' -  Table: ' + sale.table + ' - Quantity: ' + sale.quantity
    ul.appendChild(li)
  }
}
  div.appendChild(ul)
  return div
}

const createRelatedWastageRecords = (data) => {
  let div = document.createElement('div')
  div.classList.add('container-fluid')
  let h5 = document.createElement('h5')
  h5.classList.add('text-center')
  h5.innerHTML = 'Releated wastages'
  div.appendChild(h5)
  let dataDiv = document.createElement('div')
  dataDiv.classList.add('list-group')
  if(data != [] && data != undefined){
    for (let wastage of data) {
      console.log(wastage)
    let anchor = document.createElement('a')
    anchor.classList.add('list-group-item', 'list-group-item-action')
    anchor.href = "/manager/wastages/" + wastage.id
    anchor.innerHTML = 'Date: ' + wastage.date + ' - Info: ' + wastage.stockmovement_info + ' - Quantity: ' + wastage.quantity
    dataDiv.appendChild(anchor)
    }
  }
  div.appendChild(dataDiv)
  return div
}

const createRelatedPreparationRecords = (data) => {
  let div = document.createElement('div')
  div.classList.add('container-fluid')
  let h5 = document.createElement('h5')
  h5.classList.add('text-center')
  h5.innerHTML = 'Releated preparations'
  div.appendChild(h5)
  let ul = document.createElement('ul')
  ul.classList.add('list-group')
  if(data != [] && data != undefined){
    for (let preparation of data) {
      let li = document.createElement('li')
      li.classList.add('list-group-item')
      li.innerHTML = 'Date: ' + preparation.date + ' - Quantity: ' + preparation.quantity
      ul.appendChild(li)
    }
  }
  div.appendChild(ul)
  return div
}

const createRelatedStockTakeRecords = (data) => {
  let div = document.createElement('div')
  div.classList.add('container-fluid')
  let h5 = document.createElement('h5')
  h5.classList.add('text-center')
  h5.innerHTML = 'Releated stock takes'
  div.appendChild(h5)
  let ul = document.createElement('ul')
  ul.classList.add('list-group')
  if(data != [] && data != undefined){
    for (let stockTake of data) {
      let li = document.createElement('li')
      li.classList.add('list-group-item')
      li.innerHTML = 'Date: ' + stockTake.date + ' - Quantity: ' + stockTake.quantity
      ul.appendChild(li)
    }
  }
  div.appendChild(ul)
  return div
}

const createRelatedRecipeRecords = (data) => {
  let div = document.createElement('div')
  div.classList.add('container-fluid')
  let h5 = document.createElement('h5')
  h5.classList.add('text-center')
  h5.innerHTML = 'Releated recipes'
  div.appendChild(h5)
  let dataDiv = document.createElement('div')
  dataDiv.classList.add('list-group')
  if(data != [] && data != undefined){
    for (let recipe of data) {
    let anchor = document.createElement('a')
    anchor.classList.add('list-group-item', 'list-group-item-action')
    anchor.href = '/manager/recipes/' + recipe.id
    anchor.innerHTML = 'Id: ' + recipe.id + ' -  Manufactored ingredient: ' + recipe.name + ' - Sellable: ' + recipe.sellable
    dataDiv.appendChild(anchor)
  }
}
  div.appendChild(dataDiv)
  return div
}

const createRelatedPlacedOrderRecords = (data) => {
  let div = document.createElement('div')
  div.classList.add('container-fluid')
  let h5 = document.createElement('h5')
  h5.classList.add('text-center')
  h5.innerHTML = 'Releated placed orders'
  div.appendChild(h5)
  let dataDiv = document.createElement('div')
  dataDiv.classList.add('list-group')
  if(data != [] && data != undefined){
    for (let placedorder of data) {
    let anchor = document.createElement('a')
    anchor.classList.add('list-group-item', 'list-group-item-action')
    anchor.href = '/suppliers/' + placedorder.supplier_id + "/placedorders/" + placedorder.id + "/view-placedorder"
    anchor.innerHTML = 'Id: ' + placedorder.id + ' -  Date: ' + placedorder.date + '  -  Quantity: ' + placedorder.quantity
    dataDiv.appendChild(anchor)
  }
}
  div.appendChild(dataDiv)
  return div
}

const createRelatedDeliveryRecords = (data) => {
  let div = document.createElement('div')
  div.classList.add('container-fluid')
  let h5 = document.createElement('h5')
  h5.classList.add('text-center')
  h5.innerHTML = 'Related deliveries'
  div.appendChild(h5)
  let dataDiv = document.createElement('div')
  dataDiv.classList.add('list-group')
  if(data != [] && data != undefined){
    for (let delivery of data) {
    let anchor = document.createElement('a')
    anchor.classList.add('list-group-item', 'list-group-item-action')
    anchor.href = '/suppliers/' + delivery.supplier_id + "/deliveries/" + delivery.id
    anchor.innerHTML = 'Id: ' + delivery.id + ' -  Date: ' + delivery.date + '  -  Quantity: ' + delivery.quantity
    dataDiv.appendChild(anchor)
  }
}
  div.appendChild(dataDiv)
  return div
}

const diplayToast = () => {
  const toastLive = document.getElementsByClassName('toast')
  if (toastLive.length > 0){
    for (let t of toastLive) {
    const toastBootstrap = bootstrap.Toast.getOrCreateInstance(t)
    toastBootstrap.show()
    }
  }
}

$(document).ready(function () {
  const toastLive = document.getElementsByClassName('toast')
  if (toastLive.length > 0){
    for (let t of toastLive) {
    const toastBootstrap = bootstrap.Toast.getOrCreateInstance(t)
    toastBootstrap.show()
    }
  }
  if (window.location.pathname === '/chef/createrecipe') {
    const inputFields = $('.view-toggle');
    for (let inputField of inputFields) {
      $(inputField).hide();
    }
    $('input[type=checkbox]').on('change', function () {
      const id = $(this).attr('id');
      if (id.includes("manufactored")) {
        itemId = '#manufactored_ingredient_quantity_' + id.split('_')[2];
      } else {
        itemId = '#ingredient_quantity_' + id.split('_')[1];
      }
      if ($(this).is(':checked')) {
        $(itemId).parent().show();
      } else {
        $(itemId).parent().hide();
      }
    });
    $('#submitform').on('click', submitRecipeForm)
  } else if (window.location.pathname.includes('/deliveries/adddelivery')) {
    const inputFields = $('.view-toggle');
    for (let inputField of inputFields) {
      $(inputField).hide();
    }
    $('input[type=checkbox]').on('change', function () {
      const id = $(this).attr('id');
      itemId = '#ingredient_quantity_' + id.split('_')[1];
      if ($(this).is(':checked')) {
        $(itemId).parent().show();
      } else {
        $(itemId).parent().hide();
      }
    });
    $('#submitform').on('click', submitAddDeliveryForm)
  } else if (window.location.pathname.includes('/placedorders/addorder')) {
    const inputFields = $('.view-toggle');
    for (let inputField of inputFields) {
      $(inputField).hide();
    }
    $('input[type=checkbox]').on('change', function () {
      const id = $(this).attr('id');
      itemId = '#ingredient_quantity_' + id.split('_')[1];
      if ($(this).is(':checked')) {
        $(itemId).parent().show();
      } else {
        $(itemId).parent().hide();
      }
    });
    if (is_manager == "True"){
      $('#submitform').on('click', submitPlaceOrderForm)
    }
  } else if (window.location.pathname === '/login') {
    $('#metamask').on('click', connectWithMetamask);
    $('#submitform').on('click', submitLoginForm)
  } else if (window.location.pathname === '/register') {
    $('#metamask').on('click', connectWithMetamask);
    $('#submitform').on('click', submitRegisterForm);
  } else if (window.location.pathname.includes('/manager/recipe')) {
    $('#edit').on('click', editRecipe);
    $('#prepare').on('click', submitPrepareRecipeForm);
  } else if (window.location.pathname.includes('/manager/stockmanagement')){
    $('.view-toggle').hide()
  } else if (window.location.pathname === '/manager/addwastages') {
    const inputFields = $('.view-toggle');
    for (let inputField of inputFields) {
      $(inputField).hide();
    }
    $('input[type=checkbox]').on('change', function () {
      const id = $(this).attr('id');
      if (id.includes("manufactored")) {
        itemId = '#manufactored_ingredient_quantity_' + id.split('_')[2];
      } else {
        itemId = '#ingredient_quantity_' + id.split('_')[1];
      }
      if ($(this).is(':checked')) {
        $(itemId).parent().show();
      } else {
        $(itemId).parent().hide();
      }
    });
    $('#submitform').on('click', submitWastageForm);
  } else if (window.location.pathname == '/manager/addemployee'){
    $('#submitform').on('click', submitHireForm);
  } else if (window.location.pathname.includes('view-placedorder')) {
    $('#submitform').on('click', submitOrderForm);
  } else if (window.location.pathname == '/dashboard'){
    $("#edit").on('click', function() {
      $("#edit_profile").css({"display": "flex"})
      $("#save").prop("disabled", false)
      $(this).prop("disabled", true)
      $("#save").on("click", async function(){
        var form = document.getElementById("edit_profile")
        var formData = new FormData(form)
        try {
          const data = await fetch(window.location.pathname, {
            method: "POST",
            body: formData
          })
          if(await data.success) {
            window.location.reload()
          }
        } catch (error) {
          console.log(error)
        }
        
      })
    })
  }
});

const addToOrder = async () => {
  const form = document.getElementById('ingredient_quantity_form')
  const formData = new FormData(form)
  const quantity = formData.get('stock')
  if(window.location.pathname == '/manager/stockmanagement'){
    formData.append('ingredient_quantity_'+ingredient['ingredient_id'], quantity)

    try  {
      const response = await fetch("/suppliers/"+ingredient['supplier_id']+"/add_to_order",{
        method: 'POST',
        body: formData
      })
      const data = await response.json()
      console.log(data)
      if  (data.success)  {
        window.location.href = '/manager/stockmanagement'
      }
    } catch  (error)  {
      console.log(error)
    }
  } else {
    formData.append('ingredient_quantity_'+$("#ingredient_id").val(), quantity)

    try  {
      const response = await fetch("/suppliers/"+$("#supplier_id").val()+"/add_to_order",{
        method: 'POST',
        body: formData
      })
      const data = await response.json()
      if  (data.success)  {
        window.location.reload()
      }
    } catch  (error)  {
      console.log(error)
    }

  }
}

const stockTakeIngredient = async () => {
  const id = ingredient.ingredient_id
  console.log(id)
  const form = document.getElementById('ingredient_quantity_form')
  const formData = new FormData(form)
  console.log(formData)
  try {
    const response = await fetch(`/manager/ingredients/${id}/setstock`,{
      method: 'POST',
      body: formData
    })
    const data = await response.json()
    if(data.success) {
      window.location.reload()
      console.log(formData)
    }
  } catch (error) {
    
  }
}

const stockTakeManufactoredIngredient = async () => {
  const id = manufactored_ingredient.manufactored_ingredient_id
  const form = document.getElementById('ingredient_quantity_form')
  const formData = new FormData(form)
  console.log(formData)
  try {
    const response = await fetch(`/manager/manufactoredingredients/${id}/setstock`,{
      method: 'POST',
      body: formData
    })
    const data = await response.json()
    if(data.success) {
      window.location.reload()
      console.log(formData)
    }
  } catch (error) {
    
  }
}

  
const switchSetStock = () => {
  if(ingredient != undefined) {
    stockTakeIngredient()
  } else {
    stockTakeManufactoredIngredient()
  }
}

const addIngredientQuantity = (is_manufactored, ingredient_id, ingredient_name) => {

  let item = ""
  let itemQuantity = ""
  let quantity;
  if(is_manufactored) {
    item = "ingredient_id_"
    itemQuantity = "ingredient_quantity_"
    quantity = "grams"
  } else {
    item = "manufactored_ingredient_id_"
    itemQuantity = "manufactored_ingredient_quantity_"
    quantity = "Portions"
  }
  const row = document.createElement('div')
  row.classList.add('row')
  const p = document.createElement('p')
  p.classList.add('col', 's7')
  const label = document.createElement('label')
  label.classList.add('brown-text', 'text-darken-4')
  const input = document.createElement('input')
  input.classList.add('myCheckbox')
  $(input).attr('type','checkbox')
  $(input).attr('name', item + ingredient_id)
  $(input).attr('id', item + ingredient_id)
  const span = document.createElement('span')
  span.innerHTML=ingredient_name
  label.appendChild(input)
  label.appendChild(span)
  p.appendChild(label)
  const inputField = document.createElement('div')
  inputField.classList.add('input-field','col','s3','push-s1','view-toggle')
  const quantityAdded = document.createElement('input')
  quantityAdded.classList.add('validate')
  $(quantityAdded).attr('type', 'number')
  $(quantityAdded).attr('name', itemQuantity + ingredient_id)
  $(quantityAdded).attr('id', itemQuantity + ingredient_id)
  $(quantityAdded).attr('placeholder', 0)
  const quantityLabel = document.createElement('label')
  quantityLabel.innerHTML=quantity
  quantityLabel.classList.add('brown-text', 'text-darken-4')
  inputField.appendChild(quantityAdded)
  inputField.appendChild(quantityLabel)
  row.appendChild(p)
  row.appendChild(inputField)
  if (is_manufactored != "M") {
    document.getElementById('ingredients').appendChild(row)
  } else {
    document.getElementById('manufactoredIngredients').appendChild(row)
  }
}
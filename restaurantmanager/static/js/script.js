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
  } else if (page === '/owner/addemployee') {
    const form = document.getElementById('register_form');
    const formData = new FormData(form);
    formData.append('web3_address', address);
    formData.append('account_type', '1');
    formData.append('email', `${address}@internal.kitchenmanager`)
    formData.append('google_id', 'EOA')
    formData.append('password', address);
    formData.append('confirm_password', address);
    formData.append('#mnemonic', "EOA");
    formData.append('#priv', "EOA");

  }


  return true;
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
  } else if (page === '/owner/addemployee') {
    const wallet = createWallet();
    const form = document.getElementById('register_form');
    const formData = new FormData(form);
    formData.append('google_id', userCredential.sub);
    formData.append('account_type', '3');
    formData.append('mnemonic', wallet.mnemonic.phrase);
    formData.append('priv', wallet.privateKey);
    formData.append('web3_address', wallet.address);
    formData.append('email', userCredential.email);
    formData.append('password', "googleaccount")
    formData.append('password_confirm', "googleaccount")
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
    if  (data.success)  {
    window.location.href = window.location.pathname;
    }
  } catch  (e)  {
    console.error(e);
  }
}

const editRecipe = () => {
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

let recipes;
let placedorders;
let deliveries;
let orders;
let waste;
let preparations;
var tabsInstance;
let ingredientData;


const getIngredientData = async (val) => {
  const ingredient_id = val.split(' ')[0]
  try {
    const response = await fetch(`/api/ingredients/${ingredient_id}/get_ingredient_data`, {
      method:  "GET",
    })
    const data = await response.json();
    ingredientData = await data;
    recipes = createRelatedRecipeRecords(ingredientData['recipes'])
    placedorders = createRelatedPlacedOrderRecords(ingredientData['placedorders'])
    deliveries = createRelatedDeliveryRecords(ingredientData['deliveries'])
    orders = createRelatedOrderRecords(ingredientData['orders'])
    waste = createRelatedWastageRecords(ingredientData['wastages'])
    preparations = createRelatedPreparationRecords(ingredientData['preparations'])
    const tabs = document.getElementById('tabs')
    var instance = M.Tabs.getInstance(tabs)
    instance.select("recipes")
  } catch (error) {
    
  }
}

const showTabData = (tabId) => {
  if (tabId == 0 && recipes != []) {
    tab = document.getElementById('recipes')
    tab.innerHTML = ''
    tab.appendChild(recipes)
  } else if  (tabId == 1 && placedorders != [])  {
    tab = document.getElementById('placedorders')
    tab.innerHTML = ''
    tab.appendChild(placedorders)
  } else if  (tabId == 2 && deliveries != [])  {
    tab = document.getElementById('deliveries')
    tab.innerHTML = ''
    tab.appendChild(deliveries)
  } else if (tabId == 3 && preparations != []) {
    tab = document.getElementById('preparations')
    tab.innerHTML = ''
    tab.appendChild(preparations)
  } else if (tabId == 4  && wastages != []) {
    tab = document.getElementById('wastages')
    tab.innerHTML = ''
    tab.appendChild(waste)
  } else if  (tabId == 5  && orders  != [])  {
    tab = document.getElementById('orders')
    tab.innerHTML = ''
    tab.appendChild(orders)
   }
}

const createRelatedOrderRecords = (data) => {
  let div = document.createElement('div')
  div.classList.add('col', 's12')
  let h5 = document.createElement('h5')
  h5.classList.add('center-align')
  h5.innerHTML = 'Releated sales'
  div.appendChild(h5)
  let dataDiv = document.createElement('div')
  dataDiv.classList.add('collection')
  if(data != undefined){
    for (let sale of data) {
    let li = document.createElement('li')
    li.classList.add('collection-item')
    li.innerHTML = 'Date: ' + sale.date + ' -  Table: ' + sale.table + ' - Quantity: ' + sale.quantity
    dataDiv.appendChild(li)
  }
}
  div.appendChild(dataDiv)
  return div
}

const createRelatedWastageRecords = (data) => {
  let div = document.createElement('div')
  div.classList.add('col', 's12')
  let h5 = document.createElement('h5')
  h5.classList.add('center-align')
  h5.innerHTML = 'Releated wastages'
  div.appendChild(h5)
  let dataDiv = document.createElement('div')
  dataDiv.classList.add('collection')
  if(data != undefined){
    for (let wastage of data) {
    let anchor = document.createElement('a')
    anchor.classList.add('collection-item')
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
  div.classList.add('col', 's12')
  let h5 = document.createElement('h5')
  h5.classList.add('center-align')
  h5.innerHTML = 'Releated preparations'
  div.appendChild(h5)
  let dataDiv = document.createElement('div')
  dataDiv.classList.add('collection')
  if(data != undefined){
    for (let preparation of data) {
      let li = document.createElement('li')
      li.classList.add('collection-item')
      li.innerHTML = 'Date: ' + preparation.date + ' - Quantity: ' + preparation.quantity
      dataDiv.appendChild(li)
    }
  }
  return div
}

const createRelatedRecipeRecords = (data) => {
  let div = document.createElement('div')
  div.classList.add('col', 's12')
  let h5 = document.createElement('h5')
  h5.classList.add('center-align')
  h5.innerHTML = 'Releated recipes'
  div.appendChild(h5)
  let dataDiv = document.createElement('div')
  dataDiv.classList.add('collection')
  if(data != undefined){
    for (let recipe of data) {
    let anchor = document.createElement('a')
    anchor.classList.add('collection-item')
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
  div.classList.add('col', 's12')
  let h5 = document.createElement('h5')
  h5.classList.add('center-align')
  h5.innerHTML = 'Releated placed orders'
  div.appendChild(h5)
  let dataDiv = document.createElement('div')
  dataDiv.classList.add('collection')
  if(data != undefined){
    for (let placedorder of data) {
    let anchor = document.createElement('a')
    anchor.classList.add('collection-item')
    anchor.href = '/manager/suppliers/' + placedorder.supplier_id + "/placedorders/" + placedorder.id
    anchor.innerHTML = 'Id: ' + placedorder.id + ' -  Date: ' + placedorder.date + '  -  Quantity: ' + placedorder.quantity
    dataDiv.appendChild(anchor)
  }
}
  div.appendChild(dataDiv)
  return div
}

const createRelatedDeliveryRecords = (data) => {
  let div = document.createElement('div')
  div.classList.add('col', 's12')
  let h5 = document.createElement('h5')
  h5.classList.add('center-align')
  h5.innerHTML = 'Related deliveries'
  div.appendChild(h5)
  let dataDiv = document.createElement('div')
  dataDiv.classList.add('collection')
  if(data != undefined){
    for (let delivery of data) {
    let anchor = document.createElement('a')
    anchor.classList.add('collection-item')
    anchor.href = '/manager/suppliers/' + delivery.supplier_id + "/deliveries/" + delivery.id
    anchor.innerHTML = 'Id: ' + delivery.id + ' -  Date: ' + delivery.date + '  -  Quantity: ' + delivery.quantity
    dataDiv.appendChild(anchor)
  }
}
  div.appendChild(dataDiv)
  return div
}

const getIngredients = async () => {
  try  {
    const response = await fetch('/api/get_all_ingredients', {
      method:  "GET",
    })
    const data = await response.json();
    console.log(data)
    const ingredients_data = {}
    for (let ingredient in data) {
      console.log(data[ingredient])
      const ingredient_in_searchbar = `${[data[ingredient]['id']]} - ${data[ingredient]['name']}`
      console.log(ingredient_in_searchbar)
      ingredients_data[ingredient_in_searchbar] = null;
    }
    $(function() {
      $('input.autocomplete').autocomplete({
        data: ingredients_data,
        limit: 7, // The max amount of results that can be shown at once. Default: Infinity.
        onAutocomplete: function (val) {
          getIngredientData(val)
        },
        minLength: 1, // The minimum length of the input for the autocomplete to start. Default: 1.
        });
    }, ingredients_data);
    return ingredients_data;
  } catch  (e)  {
    console.error(e);
  }
}

$(document).ready(function () {
  $('.sidenav').sidenav();
  $('select').formSelect();
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
    $('#submitform').on('click', submitPlaceOrderForm)
  } else if (window.location.pathname === '/login') {
    $('#metamask').on('click', connectWithMetamask);
    $('#submitform').on('click', submitLoginForm);
  } else if (window.location.pathname === '/register') {
    $('#metamask').on('click', connectWithMetamask);
    $('#submitform').on('click', submitRegisterForm);
  } else if (window.location.pathname.includes('/manager/recipe')) {
    $('#edit').on('click', editRecipe);
  } else if (window.location.pathname.includes('/manager/stockmanagement')){
    $('.view-toggle').hide()
    getIngredients();
    if (tabsInstance === undefined)
    $(function() {
      tabsInstance = M.Tabs.init(tabs,{
        duration: 1000,
        onShow: function () {
          tab = tabsInstance.index
          showTabData(tab)
        },
      });
    });
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
  }
});
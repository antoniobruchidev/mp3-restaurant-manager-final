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
  console.log(name, description, itemkind);
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

let recipes;
let placedorders;
let deliveries;

var tabsInstance;
const getIngredientData = async (val) => {
  const ingredient_id = val.split(' ')[0]
  try {
    const response = await fetch(`/api/ingredients/${ingredient_id}/get_ingredient_data`, {
      method:  "GET",
    })
    const data = await response.json();
    recipes = createRelatedRecipeRecords(await data['recipes'])
    placedorders = createRelatedPlacedOrderRecords(await data['placedorders'])
    deliveries = createRelatedDeliveryRecords(await data['deliveries'])
    const tabs = document.getElementById('tabs')
    var instance = M.Tabs.getInstance(tabs)
    instance.select("recipes")
  } catch (error) {
    
  }
}

const showTabData = (tabId) => {
  if (tabId == 0 && recipes != []) {
    tab = document.getElementById('recipes')
    tab.innerHTML = '<h5 class="center-align">Related recipes</h5>'
    tab.appendChild(recipes)
  } else if  (tabId == 1 && placedorders != [])  {
    tab = document.getElementById('placedorders')
    tab.innerHTML = '<h5 class="center-align">Related placed orders</h5>'
    tab.appendChild(placedorders)
    console.log(placedorders)
  } else if  (tabId == 2 && deliveries != [])  {
    tab = document.getElementById('deliveries')
    tab.innerHTML = '<h5 class="center-align">Related deliveries</h5>'
    tab.appendChild(deliveries)
  }
}

const createRelatedRecipeRecords = (data) => {
  let row = document.createElement('div')
  row.classList.add('row')
  for (let recipe of data) {
  let col = document.createElement('div')
  col.classList.add('col', 's3', 'push-s1')
  let card = document.createElement('div')
  card.classList.add('card',  'blue-grey',  'darken-1')
  let cardContent = document.createElement('div')
  cardContent.classList.add('card-content',  'white-text')
  let cardTitle = document.createElement('span')
  cardTitle.classList.add('card-title')
  cardTitle.innerHTML = recipe.name + ' ID: ' + recipe.id
  let cardText = document.createElement('p')
  cardText.innerHTML = recipe.description
  let cardActions = document.createElement('div')
  cardActions.classList.add('card-action')
  let anchor = document.createElement('a.')
  cardActions.appendChild(anchor)
  cardContent.appendChild(cardTitle)
  cardContent.appendChild(cardText)
  card.appendChild(cardContent)
  card.appendChild(cardActions)
  col.appendChild(card)
  row.appendChild(col)
  }
  return row
}

const createRelatedPlacedOrderRecords = (data) => {
  let row = document.createElement('div')
  row.classList.add('row')
  for (let placedorder of data) {
  let col = document.createElement('div')
  col.classList.add('col', 's3', 'push-s1')
  let card = document.createElement('div')
  card.classList.add('card',  'blue-grey',  'darken-1')
  let cardContent = document.createElement('div')
  cardContent.classList.add('card-content',  'white-text')
  let cardTitle = document.createElement('span')
  cardTitle.classList.add('card-title')
  cardTitle.innerHTML = placedorder.date + ' ID: ' + placedorder.id
  let cardText = document.createElement('p')
  cardText.innerHTML = placedorder.quantity
  let cardActions = document.createElement('div')
  cardActions.classList.add('card-action')
  let anchor = document.createElement('a.')
  cardActions.appendChild(anchor)
  cardContent.appendChild(cardTitle)
  cardContent.appendChild(cardText)
  card.appendChild(cardContent)
  card.appendChild(cardActions)
  col.appendChild(card)
  row.appendChild(col)
  }
  return row
}

const createRelatedDeliveryRecords = (data) => {
  let row = document.createElement('div')
  row.classList.add('row')
  for (let delivery of data) {
  let col = document.createElement('div')
  col.classList.add('col', 's3', 'push-s1')
  let card = document.createElement('div')
  card.classList.add('card',  'blue-grey',  'darken-1')
  let cardContent = document.createElement('div')
  cardContent.classList.add('card-content',  'white-text')
  let cardTitle = document.createElement('span')
  cardTitle.classList.add('card-title')
  cardTitle.innerHTML = delivery.date + ' ID: ' + delivery.id
  let cardText = document.createElement('p')
  cardText.innerHTML = delivery.quantity
  let cardActions = document.createElement('div')
  cardActions.classList.add('card-action')
  let anchor = document.createElement('a.')
  cardActions.appendChild(anchor)
  cardContent.appendChild(cardTitle)
  cardContent.appendChild(cardText)
  card.appendChild(cardContent)
  card.appendChild(cardActions)
  col.appendChild(card)
  row.appendChild(col)
  }
  console.log(row)
  return row
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
    $(function() {
      tabsInstance = M.Tabs.init(tabs,{
        duration: 1000,
        onShow: function () {
          tab = tabsInstance.index
          showTabData(tab)
        },
      });
    });
  }
});


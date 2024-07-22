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
  const address =  await accounts[0];

  // The MetaMask plugin also allows signing transactions to
  // send ether and pay to change state within the blockchain.
  // For this, you need the account signer...
  const signer = provider.getSigner()

  const page = window.location.pathname;
  if (page === '/login') {
    $('#web3_address').val(address);
    $('#submit').click();
  } else if (page === '/register') {
    $('#web3_address').val(address);
    $('#email').val(`${address}@internal.kitchenmanager`);
    $('#f_name').val('EOA')
    $('#l_name').val('EOA')
    $('#google_id').val('EOA')
    $('#password').val(address);
    $('#confirm_password').val(address);
    $('#mnemonic').val("EOA");
    $('#priv').val("EOA");
    $('#submit').click();
  } else if  (page === '/owner/addemployee') {
    $('#web3_address').val(address);
    $('#email').val(`${address}@internal.kitchenmanager`);
    $('#google_id').val('EOA')
    $('#password').val(address);
    $('#confirm_password').val(address);
    $('#mnemonic').val("EOA");
    $('#priv').val("EOA");
  }


  return true;
}

  /**
 * Function to handle Google Signin response
 * @param {*} response 
 */
function handleCredentialResponse(response) {
  const page = window.location.pathname;
  const userCredential = decodeJWT(response.credential);
  if (page === '/login') {
    $('#google_id').val(userCredential.sub);
    $('#submit').click();
  } else if (page === '/register') {
    const wallet = createWallet();
    $('#web3_address').val(wallet.address);
    $('#priv').val(wallet.privateKey);
    $('#mnemonic').val(wallet.mnemonic.phrase);
    $('#f_name').val(userCredential.given_name);
    $('#l_name').val(userCredential.family_name);
    $('#google_id').val(userCredential.sub);
    $('#email').val(userCredential.email);
    $('#password').val("googleaccount");
    $('#confirm_password').val("googleaccount");
    $('#submit').click();
  } else if  (page === '/owner/addemployee') {
    const wallet = createWallet();
    $('#web3_address').val(wallet.address);
    $('#priv').val(wallet.privateKey);
    $('#mnemonic').val(wallet.mnemonic.phrase);
    $('#google_id').val(userCredential.sub);
    $('#email').val(userCredential.email);
    $('#password').val("googleaccount");
    $('#confirm_password').val("googleaccount");
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

/**
 * Event listener to handle the user's choice of account type
 */
const handleConnectionChoice = () => {
  const page = window.location.pathname;
  if ($('#account_type').val() === '1') {
    connectWithMetamask();
  } else if ($('#account_type').val() === '2') {
    const wallet = createWallet();
    $('#web3_address').val(wallet.address);
    $('#priv').val(wallet.privateKey);
    $('#mnemonic').val(wallet.mnemonic.phrase);  
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

const submitAddDeliveryForm = async () =>  {
  const form = document.getElementById('add_delivery_form');
  console.log(form)
  const formData = new FormData(form);
  try {
    const response = await fetch(window.location.pathname,  {
      method: "POST",
      body: formData,
    })
    const data = await response.json();
    if  (data.success)  {
      window.location.href = window.location.pathname;
    }
  } catch (e) {
    console.error(e);
  }
}

$(document).ready(function(){
  $('.sidenav').sidenav();
  $('select').formSelect();
  $('#account_type').on('change', handleConnectionChoice);
  if (window.location.pathname === '/chef/createrecipe') {
    const inputFields = $('.view-toggle');
    for (let inputField of inputFields) {
      $(inputField).hide();
    }
    $('input[type=checkbox]').on('change', function(){
      const id = $(this).attr('id');
      if (id.includes("manufactored")){
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
    for  (let inputField of inputFields)  {
      $(inputField).hide();
    }
    $('input[type=checkbox]').on('change', function(){
      const id = $(this).attr('id');
      itemId = '#ingredient_quantity_'+ id.split('_')[1];
      if ($(this).is(':checked')) {
        $(itemId).parent().show();
      } else {
        $(itemId).parent().hide();
      }
    });
    $('#submitform').on('click', submitAddDeliveryForm)
  } else if (window.location.pathname.includes('/orders/addorder')) {
    const inputFields = $('.view-toggle');
    for (let inputField of inputFields) {
      $(inputField).hide();
    }
    $('input[type=checkbox]').on('change', function(){
      const id = $(this).attr('id');
      itemId = '#ingredient_quantity_'+ id.split('_')[1];
      if  ($(this).is(':checked')) {
        $(itemId).parent().show();
      } else  {
        $(itemId).parent().hide();
      }
    });
    $('#submitform').on('click', submitPlaceOrderForm)
  }
});


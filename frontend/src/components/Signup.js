import React from "react";

const Signup = () => {
  return (
    <div>
      <h1>Signup</h1>
      <form>
        <div>
          <label>First Name</label>
          <input type="text" placeholder="First Name" />
        </div>
        <div>
          <label>Last Name</label>
          <input type="text" placeholder="Last Name" />
        </div>
        <div>
          <label>Email</label>
          <input type="email" placeholder="Email" />
        </div>
        <div>
          <label>Password</label>
          <input type="password" placeholder="Password" />
        </div>
        <button type="submit">Signup</button>
      </form>
    </div>
  );
};

export default Signup;

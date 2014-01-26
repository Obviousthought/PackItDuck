<div class="navbar">
  <div class="navbar-inner">
    <div class="container">
      <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </a>
      <a class="navbar-brand" href="/">PackingZen</a>
      <div class="nav-collapse">
        <ul class="nav">
          <li><a href="{{url_for('profile', username=current_user.username)}}">Home</a></li>
            <li><a href="/new_trip">New Trip</a></li>
          </li>
        </ul>    
            <ul class="nav pull-right">
          <li class="divider-vertical"></li>
          <li><form id="custom-search-form" class="form-search form-horizontal pull-right">
                <div class="input-append span12">
                    <input type="text" class="search-query" placeholder="Search">
                    <button type="submit" class="btn"><i class="icon-search"></i></button>
                </div>
              </form></li>
          <li class="dropdown">
            <a href="#" class="dropdown-toggle" data-toggle="dropdown">{{current_user.username}} <b class="caret"></b></a>
            <ul class="dropdown-menu">
              <li><a href="/settings">Settings</a></li>
              <li class="divider"></li>
              <li><a href="/logout">Logout</a></li>
            </ul>
          </li>
        </ul>
      </div><!-- /.nav-collapse -->
    </div>
  </div><!-- /navbar-inner -->
</div>
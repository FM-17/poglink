from poglink.utils import setup_argparse, parse_list


def test_parse_list():
    assert parse_list("this,       is,  a  , test    ") == ["this", "is", "a", "test"]
    assert parse_list("") == [""]
    assert parse_list("this,has,a,double,,comma") == [
        "this",
        "has",
        "a",
        "double",
        "",
        "comma",
    ]


def test_parser():
    parser = setup_argparse()

    args = parser.parse_args(
        [
            "-d",
            "~/data-dir",
            "-t",
            "MYTOKEN",
            "-p",
            "500",
            "-a",
            "test,admin",
            "--rates-urls",
            "www.test.com,www.test123.com",
            "--rates-channel-id",
            "1234",
            "--bans-url",
            "www.bans.com",
            "--bans-channel-id",
            "4321",
            "--debug",
        ]
    )

    assert args.data_dir == "~/data-dir"
    assert args.token == "MYTOKEN"
    assert args.polling_delay == 500
    assert args.allowed_roles == ["test", "admin"]
    assert args.rates_urls == ["www.test.com", "www.test123.com"]
    assert args.rates_channel_id == "1234"
    assert args.bans_url == "www.bans.com"
    assert args.bans_channel_id == "4321"
    assert args.debug == True

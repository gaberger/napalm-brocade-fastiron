Value Username ((\d+\.){3}\d+)
Value Password (\S+)
Value Encrypt (\S+)
Value Privilege (\d+)
Value Status (\S+)
Value Expiry (\S+)

Start
  ^${Username}\s+${Password}\s+${Encrypt}\s+${Privilege}\s+${Status}\s+${Expiry} ->  Next.Record
